import re
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def parse_document(html: str) -> str:
    """Convert DART HTML disclosure to clean plaintext for Claude."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove style and script blocks
    for tag in soup(["style", "script", "meta", "head"]):
        tag.decompose()

    # Extract title from <title> tag if present
    title_text = ""
    title_tag = BeautifulSoup(html, "html.parser").find("title")
    if title_tag:
        # title format: "Company/ReportName/(date)ReportName"
        parts = title_tag.get_text().split("/")
        if len(parts) >= 2:
            title_text = f"[{parts[1].strip()}]\n\n"

    lines = []
    if title_text:
        lines.append(title_text.strip())

    for table in soup.find_all("table"):
        table_lines = _parse_table(table)
        if table_lines:
            lines.append(table_lines)
        table.decompose()

    # Remaining free text outside tables
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n")
        text = _clean_whitespace(text)
        if text:
            lines.append(text)

    return "\n\n".join(lines)


def _parse_table(table) -> str:
    rows = []
    for tr in table.find_all("tr"):
        cells = [_cell_text(td) for td in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c and c != "-"]
        if cells:
            rows.append(" | ".join(cells))

    # Drop rows that are pure dash/noise
    rows = [r for r in rows if not re.fullmatch(r"[\s\-|]+", r)]
    return "\n".join(rows)


def _cell_text(tag) -> str:
    text = tag.get_text(separator=" ", strip=True)
    # Collapse internal whitespace and line breaks
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clean_whitespace(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()
