import json
from pathlib import Path

from ranx import Qrels, Run, evaluate

from app.backend.embeddings import (
    get_embeddings_model
)

from app.backend.rag.hybrid_retriever import (
    HybridRetriever
)

from app.backend.search.client import (
    get_opensearch_client
)


QUESTIONS_PATH = (
    Path(__file__).parent
    / "questions.json"
)


def load_questions():
    with open(
        QUESTIONS_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():

    questions = load_questions()

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    retriever = HybridRetriever(
        client=client,
        embedding_model=embeddings
    )


    qrels_data = {}
    run_data = {}

    top1_misses = []


    for item in questions:

        query_id = item["id"]

        expected_documents = set(
            item["expected_documents"]
        )


        # Ground-truth documents
        qrels_data[query_id] = {
            document_id: 1
            for document_id
            in expected_documents
        }


        # Run real hybrid retrieval
        results = retriever.retrieve(
            query=item["question"],
            k=5
        )


        # Documents returned by retriever
        retrieved_documents = []

    for hit in results:

        document_id = (
            hit["_source"]["document_id"]
        )

        if document_id not in retrieved_documents:

            retrieved_documents.append(
                document_id
            )


        # -----------------------------
        # Top-1 Error Analysis
        # -----------------------------

        top1_document = (
            retrieved_documents[0]
            if retrieved_documents
            else None
        )


        if top1_document not in expected_documents:

            expected_rank = None

            for rank, document_id in enumerate(
                retrieved_documents,
                start=1
            ):

                if document_id in expected_documents:

                    expected_rank = rank

                    break


            top1_misses.append(
                {
                    "id": query_id,

                    "question":
                        item["question"],

                    "expected":
                        item[
                            "expected_documents"
                        ],

                    "top1":
                        top1_document,

                    "expected_rank":
                        expected_rank
                }
            )


        # -----------------------------
        # Prepare run for ranx
        # -----------------------------

        documents = {}


        for hit in results:

            document_id = (
                hit["_source"]["document_id"]
            )

            score = float(
                hit["_score"]
            )


            # Multiple chunks may belong
            # to the same document.
            #
            # For document-level evaluation,
            # keep the highest score.
            if (
                document_id not in documents
                or
                score > documents[document_id]
            ):

                documents[document_id] = score


        run_data[query_id] = documents


    # -----------------------------
    # Calculate retrieval metrics
    # -----------------------------

    qrels = Qrels(
        qrels_data
    )

    run = Run(
        run_data
    )


    scores = evaluate(
        qrels,
        run,
        [
            "hit_rate@1",
            "hit_rate@3",
            "hit_rate@5",
            "mrr@5",
            "ndcg@5"
        ]
    )


    # -----------------------------
    # Print results
    # -----------------------------

    print(
        "\nRetrieval Evaluation"
    )

    print(
        "=" * 40
    )


    print(
        f"Queries         "
        f"{len(questions)}"
    )


    for metric, score in scores.items():

        print(
            f"{metric:<15} "
            f"{score:.4f}"
        )


    # -----------------------------
    # Error Analysis
    # -----------------------------

    print(
        "\nTop-1 Error Analysis"
    )

    print(
        "=" * 40
    )


    if not top1_misses:

        print(
            "No Top-1 retrieval errors."
        )

    else:

        print(
            f"Top-1 misses: "
            f"{len(top1_misses)}"
        )


        for miss in top1_misses:

            print(
                "\n"
                + "-" * 40
            )

            print(
                f"Query ID: "
                f"{miss['id']}"
            )

            print(
                f"Question: "
                f"{miss['question']}"
            )


            print(
                "Expected:"
            )

            for document in miss["expected"]:

                print(
                    f"  - {document}"
                )


            print(
                f"Top-1 result: "
                f"{miss['top1']}"
            )


            if (
                miss["expected_rank"]
                is not None
            ):

                print(
                    f"Expected document rank: "
                    f"{miss['expected_rank']}"
                )

            else:

                print(
                    "Expected document was not "
                    "found in Top-5."
                )


if __name__ == "__main__":

    main()