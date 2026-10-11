from pathlib import Path
import pymupdf
from docx import Document
from src.resume_parser import parse_resume
import json
from dataclasses import asdict

def extract_text_from_file(filename: str) -> str:
    """Extract text from a TXT, PDF, or DOCX resume."""

    path = Path(filename)
    extension = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    if extension == ".txt":
        return path.read_text(encoding="utf-8")

    elif extension == ".pdf":
        text_parts = []

        with pymupdf.open(path) as pdf:
            for page in pdf:
                text_parts.append(page.get_text())

        return "\n".join(text_parts)

    elif extension == ".docx":
        document = Document(path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            "Use TXT, PDF, or DOCX."
        )

def load_resume_from_file(filename: str):
    """Read a resume file and return a Candidate object."""

    text = extract_text_from_file(filename)

    if not text.strip():
        raise ValueError("The resume contains no extractable text.")

    return parse_resume(text)


def save_analysis_result(
    candidate,
    job,
    result,
    filename: str = "data/analysis_results.json"
) -> None:
    """Save a candidate analysis result to a JSON file."""

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load previous results if the file already exists.
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as file:
                saved_results = json.load(file)

            if not isinstance(saved_results, list):
                raise ValueError(
                    "The JSON file must contain a list of results."
                )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "The existing JSON file contains invalid data."
            ) from exc
    else:
        saved_results = []

    # Convert the dataclass objects into dictionaries.
    record = {
        "candidate": asdict(candidate),
        "job": asdict(job),
        "result": asdict(result),
    }

    saved_results.append(record)

    with path.open("w", encoding="utf-8") as file:
        json.dump(saved_results, file, indent=4, ensure_ascii=False)


def load_analysis_results(
    filename: str = "data/analysis_results.json"
) -> list[dict]:
    """Load previously saved candidate analysis results."""

    path = Path(filename)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "The JSON file must contain a list of results."
        )

    return data
