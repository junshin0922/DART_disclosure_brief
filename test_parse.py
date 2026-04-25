"""Test parser on SK Hynix earnings filing."""
from dart.fetcher import fetch_document
from dart.parser import parse_document

xml = fetch_document("20260423800001")
text = parse_document(xml)
print(text)
