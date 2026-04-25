import time
import logging
from datetime import datetime

from config import POLL_INTERVAL_SECONDS
from db import init_db, is_seen, mark_seen
from dart.fetcher import fetch_today_filings, fetch_document
from dart.parser import parse_document
from summarizer import is_material, summarize
from telegram.bot import dispatch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def process_filing(filing: dict) -> None:
    rcept_no = filing["rcept_no"]

    if is_seen(rcept_no):
        return

    if not is_material(filing["report_nm"]):
        log.info("SKIP  %s — %s", filing["corp_name"], filing["report_nm"].strip())
        mark_seen(rcept_no, filing["corp_code"], filing["report_nm"], filing["rcept_dt"])
        return

    log.info("NEW   %s — %s", filing["corp_name"], filing["report_nm"].strip())

    html = fetch_document(rcept_no)
    if not html:
        log.warning("Could not fetch document for %s", rcept_no)
        return

    text = parse_document(html)
    summary = summarize(filing, text)
    if not summary:
        log.warning("Summarization failed for %s", rcept_no)
        return

    ok = dispatch(filing, summary)
    if ok:
        log.info("SENT  %s", rcept_no)
    else:
        log.error("SEND FAILED %s", rcept_no)

    mark_seen(rcept_no, filing["corp_code"], filing["report_nm"], filing["rcept_dt"])


def run() -> None:
    init_db()
    log.info("Disclosure Brief started. Poll interval: %ds", POLL_INTERVAL_SECONDS)

    while True:
        log.info("--- Polling DART [%s] ---", datetime.now().strftime("%H:%M:%S"))
        try:
            filings = fetch_today_filings()
            log.info("Fetched %d filing(s) from watchlist", len(filings))
            for filing in filings:
                process_filing(filing)
        except Exception as e:
            log.error("Poll cycle error: %s", e)

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
