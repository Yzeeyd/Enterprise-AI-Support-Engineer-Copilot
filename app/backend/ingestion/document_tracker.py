import hashlib
import json
from pathlib import Path

def calculate_file_hash(file_path: str) -> str:
    with open(file_path, "rb") as file:
        content = file.read()

    return hashlib.sha256(content).hexdigest()

def get_document_id(file_path: str, documents_folder: str) -> str:
    file = Path(file_path).resolve()
    root = Path(documents_folder).resolve()

    return str(file.relative_to(root))

def file_exists(file_id: str) -> bool:
    """Check if a file exists at the given path."""


    return Path(file_id).is_file()

def save_index_state(state_path: str, state: dict) -> None:
    path = Path(state_path)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            state,
            file,
            ensure_ascii=False,
            indent=4
        )

def load_index_state(state_path: str) -> dict:
    path = Path(state_path)

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_document_status(
    document_id: str,
    current_hash: str,
    state: dict
) -> str:

    old_document = state.get(document_id)

    if old_document is None:
        return "new"

    if old_document["hash"] == current_hash:
        return "unchanged"

    return "changed"


