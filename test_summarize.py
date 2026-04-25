"""End-to-end test: fetch → parse → summarize (SK Hynix earnings)."""
from dart.fetcher import fetch_document
from dart.parser import parse_document
from summarizer import summarize
import json

filing = {
    "rcept_no": "20260423800001",
    "corp_name": "SK Hynix",
    "report_nm": "연결재무제표기준영업(잠정)실적(공정공시)",
    "rcept_dt": "20260423",
}

print("Fetching + parsing...")
html = fetch_document(filing["rcept_no"])
text = parse_document(html)

print("Summarizing with Claude Haiku...")
result = summarize(filing, text)

print(json.dumps(result, indent=2, ensure_ascii=False))
