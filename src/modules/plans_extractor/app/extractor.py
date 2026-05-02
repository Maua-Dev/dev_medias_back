import io
import logging

import pdfplumber

logger = logging.getLogger(__name__)

REPEATED_HEADER_MARKERS = (
    "INSTITUTO MAUÁ DE TECNOLOGIA",
    "PLANO DE ENSINO",
    "Página:",
    "IDENTIFICAÇÃO",
)


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract normalized text from a PDF kept entirely in memory."""
    lines: list[str] = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            if not page_text:
                logger.debug("Page %s did not contain extractable text", page_number)
                continue

            for raw_line in page_text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                if any(marker in line for marker in REPEATED_HEADER_MARKERS):
                    continue
                lines.append(line)

    return "\n".join(lines)
