"""Dump full XML of a specific filing to inspect structure."""
from dart.fetcher import fetch_document

# SK Hynix 잠정실적 — most informative for our use case
rcept_no = "20260423800001"
xml = fetch_document(rcept_no)
print(xml)
