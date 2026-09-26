class QueryRouter:

    GREETINGS = {
        "مرحبا",
        "مرحباً",
        "هلا",
        "هلا والله",
        "السلام عليكم",
        "السلام عليكم ورحمة الله وبركاته",
        "اهلا",
        "أهلا",
        "hello",
        "hi",
        "hey"
    }

    def classify(self, query: str) -> str:

        normalized = (
            query
            .strip()
            .lower()
        )

        if normalized in self.GREETINGS:
            return "greeting"

        return "rag"