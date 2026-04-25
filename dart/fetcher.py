import io
import zipfile
import requests
from datetime import date
from config import DART_API_KEY, WATCHLIST

DART_BASE = "https://opendart.fss.or.kr/api"


def fetch_today_filings() -> list[dict]:
    """Return new filings from DART for watchlist companies filed today."""
    today = date.today().strftime("%Y%m%d")
    results = []

    for corp_code, corp_name in WATCHLIST.items():
        params = {
            "crtfc_key": DART_API_KEY,
            "corp_code": corp_code,
            "bgn_de": today,
            "end_de": today,
            "page_count": 40,
        }
        try:
            resp = requests.get(f"{DART_BASE}/list.json", params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[fetcher] {corp_name} list fetch failed: {e}")
            continue

        if data.get("status") != "000":
            continue  # no filings or API error

        for item in data.get("list", []):
            results.append({
                "rcept_no":  item["rcept_no"],
                "corp_code": corp_code,
                "corp_name": corp_name,
                "report_nm": item["report_nm"],
                "rcept_dt":  item["rcept_dt"],
                "flr_nm":    item.get("flr_nm", ""),
            })

    return results


def fetch_document(rcept_no: str) -> str | None:
    """Fetch and unzip the XML document for a given receipt number.

    DART returns a ZIP archive containing <rcept_no>.xml.
    """
    params = {
        "crtfc_key": DART_API_KEY,
        "rcept_no": rcept_no,
    }
    try:
        resp = requests.get(f"{DART_BASE}/document.xml", params=params, timeout=15)
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
            xml_name = next(n for n in zf.namelist() if n.endswith(".xml"))
            return zf.read(xml_name).decode("utf-8")
    except Exception as e:
        print(f"[fetcher] document fetch failed for {rcept_no}: {e}")
        return None
