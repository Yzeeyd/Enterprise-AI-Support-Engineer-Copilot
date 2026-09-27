from pathlib import Path

from app.backend.llm import get_llm


class RAGService:

    def __init__(
        self,
        retriever,
        llm=None
    ):
        self.retriever = retriever
        self.llm = llm or get_llm()

    def ask(
        self,
        question: str,
        k: int = 5
    ) -> dict:

        hits = self.retriever.retrieve(
            query=question,
            k=k
        )

        if not hits:
            return {
                "answer": (
                    "لم أجد معلومات كافية "
                    "للإجابة على السؤال."
                ),
                "sources": []
            }

        source_map, sources = (
            self._prepare_sources(hits)
        )

        context = self._build_context(
            hits=hits,
            source_map=source_map
        )

        prompt = self._build_prompt(
            question=question,
            context=context
        )

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": sources
        }

    def _prepare_sources(
        self,
        hits: list
    ) -> tuple[dict, list[dict]]:

        source_map = {}
        sources_by_document = {}

        for hit in hits:

            source = hit["_source"]

            document_id = source.get(
                "document_id",
                "unknown"
            )

            chunk_id = source.get(
                "chunk_id"
            )

            score = hit.get(
                "_score"
            )

            metadata = source.get(
                "metadata",
                {}
            )

            if document_id not in source_map:

                source_number = (
                    len(source_map) + 1
                )

                source_map[document_id] = (
                    source_number
                )

                filename = metadata.get(
                    "filename"
                )

                if not filename:
                    filename = Path(
                        document_id
                    ).name

                sources_by_document[
                    document_id
                ] = {
                    "id": source_number,
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_ids": [],
                    "score": score
                }

            document_source = (
                sources_by_document[
                    document_id
                ]
            )

            if chunk_id:
                document_source[
                    "chunk_ids"
                ].append(chunk_id)

            if (
                score is not None
                and (
                    document_source["score"]
                    is None
                    or score
                    > document_source["score"]
                )
            ):
                document_source[
                    "score"
                ] = score

        sources = sorted(
            sources_by_document.values(),
            key=lambda item: item["id"]
        )

        return source_map, sources

    def _build_context(
        self,
        hits: list,
        source_map: dict
    ) -> str:

        context_parts = []

        for hit in hits:

            source = hit["_source"]

            document_id = source.get(
                "document_id",
                "unknown"
            )

            content = source.get(
                "content",
                ""
            )

            metadata = source.get(
                "metadata",
                {}
            )

            source_number = (
                source_map[document_id]
            )

            filename = metadata.get(
                "filename"
            )

            if not filename:
                filename = Path(
                    document_id
                ).name

            page = metadata.get(
                "page"
            )

            header = (
                f"[{source_number}] "
                f"{filename}"
            )

            if page is not None:
                header += (
                    f" | Page {page + 1}"
                )

            context_parts.append(
                f"""
                {header}

                {content}
                """.strip()
            )

        return "\n\n".join(
            context_parts
        )

    def _build_prompt(
        self,
        question: str,
        context: str
    ) -> str:

        return f"""
            You are an enterprise support assistant.

            Answer the user's question using ONLY
            the provided context.

            Rules:
            - Do not use outside knowledge.
            - Do not invent policies or procedures.
            - If the context does not contain enough
            information, clearly say so.
            - Answer in the same language as the user.
            - Be clear and concise.
            - Cite the supporting source using its
            source number, for example [1] or [2].
            - Put citations directly after the claim
            they support.
            - Only use source numbers that appear
            in the provided context.
            - Do not create fake citations.

            Context:
            {context}

            User question:
            {question}

            Answer:
            """.strip()


if __name__ == "__main__":

    from app.backend.search.client import (
        get_opensearch_client
    )

    from app.backend.embeddings import (
        get_embeddings_model
    )

    from app.backend.rag.hybrid_retriever import (
        HybridRetriever
    )

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    retriever = HybridRetriever(
        client=client,
        embedding_model=embeddings
    )

    rag = RAGService(
        retriever=retriever
    )

    result = rag.ask(
        "كيف أغير كلمة المرور؟",
        k=5
    )

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(
            f"[{source['id']}] "
            f"{source['filename']}"
        )

        print(
            f"Chunks: "
            f"{source['chunk_ids']}"
        )

        print(
            f"Retrieval score: "
            f"{source['score']}"
        )

        print("-" * 60)