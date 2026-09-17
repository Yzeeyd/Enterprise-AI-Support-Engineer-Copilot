import re


def tokenize(text: str) -> list[str]:

    text = text.lower()

    text = re.sub(
        r"[^\w\u0600-\u06FF\-]+",
        " ",
        text
    )

    return text.split()