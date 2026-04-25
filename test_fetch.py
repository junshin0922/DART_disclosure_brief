"""Quick smoke test — run with: python test_fetch.py"""
from db import init_db
from dart.fetcher import fetch_today_filings, fetch_document

init_db()

print("Fetching today's filings for watchlist companies...")
filings = fetch_today_filings()

if not filings:
    print("No filings found today (market may be closed or no new disclosures yet).")
else:
    print(f"\nFound {len(filings)} filing(s):\n")
    for f in filings:
        print(f"  [{f['rcept_dt']}] {f['corp_name']} — {f['report_nm']} (rcept_no: {f['rcept_no']})")

    # Fetch the XML of the first one to verify document API works
    first = filings[0]
    print(f"\nFetching document for: {first['report_nm']}...")
    xml = fetch_document(first["rcept_no"])
    if xml:
        print(f"  Document fetched: {len(xml):,} chars")
        print(f"  Preview: {xml[:300]!r}")
    else:
        print("  Document fetch failed.")
