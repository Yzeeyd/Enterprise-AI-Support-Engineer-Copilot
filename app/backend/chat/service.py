from app.backend.chat.router import QueryRouter


class ChatService:

    def __init__(
        self,
        rag_service,
        router=None
    ):
        self.rag_service = rag_service
        self.router = (
            router or QueryRouter()
        )

    def ask(
        self,
        question: str,
        k: int = 5
    ) -> dict:

        intent = self.router.classify(
            question
        )

        if intent == "greeting":

            return {
                "answer": (
                    "مرحباً! كيف يمكنني "
                    "مساعدتك في الدعم التقني؟"
                ),
                "sources": []
            }

        return self.rag_service.ask(
            question=question,
            k=k
        )