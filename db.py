import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).parent / "filings.db"))


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_filings (
                rcept_no TEXT PRIMARY KEY,
                corp_code TEXT NOT NULL,
                report_nm TEXT NOT NULL,
                rcept_dt  TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


def is_seen(rcept_no: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_filings WHERE rcept_no = ?", (rcept_no,)
        ).fetchone()
    return row is not None


def mark_seen(rcept_no: str, corp_code: str, report_nm: str, rcept_dt: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_filings (rcept_no, corp_code, report_nm, rcept_dt) VALUES (?, ?, ?, ?)",
            (rcept_no, corp_code, report_nm, rcept_dt),
        )
