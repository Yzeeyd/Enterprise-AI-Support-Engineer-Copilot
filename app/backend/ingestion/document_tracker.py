import hashlib
import json
from pathlib import Path


def calculate_file_hash(
    file_path: str
) -> str:

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        for block in iter(lambda: file.read(1024 * 1024),b""):
            sha256.update(block)

    return sha256.hexdigest()


def get_document_id(
    file_path: str,
    documents_folder: str
) -> str:

    file = Path(file_path).resolve()
    root = Path(documents_folder).resolve()

    return (
        file
        .relative_to(root)
        .as_posix()
    )


def save_index_state(
    state_path,
    state: dict
) -> None:

    path = Path(state_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_index_state(
    state_path
) -> dict:

    path = Path(state_path)

    if not path.exists():
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def get_document_status(
    document_id: str,
    current_hash: str,
    state: dict
) -> str:

    old_document = state.get(
        document_id
    )

    if old_document is None:
        return "new"

    if (
        old_document.get("hash")
        == current_hash
    ):
        return "unchanged"

    return "changed"