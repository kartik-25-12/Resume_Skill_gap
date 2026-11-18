"""
core/parser.py
Robust multi-format document parser supporting PDF, DOCX, and TXT.
Cleans whitespace, handles control characters, and normalizes extracted text.
"""

import io
import re
from typing import BinaryIO, Union

import docx
import pypdf


def clean_text(raw_text: str) -> str:
    """
    Cleans raw extracted text:
    - Normalizes non-ASCII/control characters
    - Collapses multiple newlines and spaces
    - Strips leading/trailing whitespace
    """
    if not raw_text:
        return ""

    # Replace strange Unicode quotes, bullets, and dashes with standard ASCII equivalents
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2022": " ", "\u2023": " ", "\u25e6": " ",
        "\u00a0": " ", "\t": " "
    }
    for old, new in replacements.items():
        raw_text = raw_text.replace(old, new)

    # Filter out non-printable/control characters (keep printable ASCII and newline)
    cleaned = "".join(
        char for char in raw_text
        if (32 <= ord(char) <= 126) or char in "\n\r"
    )

    # Collapse multiple consecutive whitespace characters (within lines) and newlines
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n\s*\n+", "\n\n", cleaned)
    return cleaned.strip()


def parse_pdf(file_stream_or_path: Union[str, BinaryIO, io.BytesIO]) -> str:
    """
    Extracts and concatenates text across all pages of a PDF document.

    Args:
        file_stream_or_path: Path to PDF or BytesIO stream (e.g., Streamlit UploadedFile).

    Returns:
        Cleaned text extracted from the PDF.

    Raises:
        ValueError: If extraction fails or document contains no extractable text.
    """
    try:
        reader = pypdf.PdfReader(file_stream_or_path)
        extracted_pages = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_pages.append(page_text)

        full_text = "\n\n".join(extracted_pages)
        cleaned = clean_text(full_text)

        if not cleaned:
            raise ValueError(
                "PDF was parsed successfully but no extractable text was found "
                "(it may be scanned/image-only)."
            )

        return cleaned
    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Failed to parse PDF document: {str(exc)}") from exc


def parse_docx(file_stream_or_path: Union[str, BinaryIO, io.BytesIO]) -> str:
    """
    Extracts text from paragraphs and tables in a Microsoft Word (.docx) document.

    Args:
        file_stream_or_path: Path to DOCX or BytesIO stream.

    Returns:
        Cleaned text extracted from the DOCX.

    Raises:
        ValueError: If extraction fails or document contains no text.
    """
    try:
        doc = docx.Document(file_stream_or_path)
        extracted_parts = []

        # Extract text from paragraphs
        for p in doc.paragraphs:
            if p.text.strip():
                extracted_parts.append(p.text.strip())

        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    extracted_parts.append(" | ".join(row_cells))

        full_text = "\n".join(extracted_parts)
        cleaned = clean_text(full_text)

        if not cleaned:
            raise ValueError("DOCX document was parsed but contains no text.")

        return cleaned
    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Failed to parse DOCX document: {str(exc)}") from exc


def extract_text(file_stream_or_path: Union[str, BinaryIO, io.BytesIO], filename: str) -> str:
    """
    Universal document text extractor that routes to appropriate parser based on file extension.
    """
    fname_lower = filename.lower()
    if fname_lower.endswith(".pdf"):
        return parse_pdf(file_stream_or_path)
    if fname_lower.endswith(".docx"):
        return parse_docx(file_stream_or_path)
    if fname_lower.endswith(".txt"):
        if isinstance(file_stream_or_path, (str, bytes)):
            if (
                isinstance(file_stream_or_path, str)
                and not file_stream_or_path.startswith("\n")
                and len(file_stream_or_path) < 1024
            ):
                try:
                    with open(file_stream_or_path, "r", encoding="utf-8", errors="ignore") as f:
                        return clean_text(f.read())
                except OSError:
                    return clean_text(file_stream_or_path)
            return clean_text(str(file_stream_or_path))

        raw = file_stream_or_path.read()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="ignore")
        return clean_text(raw)

    raise ValueError(
        f"Unsupported file format: '{filename}'. Please upload a .pdf, .docx, or .txt file."
    )
