import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

DART_URL = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"


def format_message(filing: dict, summary: dict) -> str:
    """Build HTML-formatted Telegram message."""
    bullets = "\n".join(f"• {b}" for b in summary["bullets"])
    dart_link = DART_URL.format(rcept_no=filing["rcept_no"])

    # Ticker tag from corp_code (5-digit KRX style)
    corp_tag = f"#{filing['corp_code']}"

    return (
        f"🏢 <b>{filing['corp_name']}</b>\n"
        f"📄 {filing['report_nm'].strip()}\n"
        f"📅 {filing['rcept_dt'][:4]}-{filing['rcept_dt'][4:6]}-{filing['rcept_dt'][6:]}\n"
        f"\n"
        f"<b>Summary</b>\n"
        f"{bullets}\n"
        f"\n"
        f"<i>{summary['market_impact']}</i>\n"
        f"\n"
        f'🔗 <a href="{dart_link}">View on DART</a>\n'
        f"#Korea #Disclosure {corp_tag}"
    )


def send_message(text: str) -> bool:
    """Send a message to the configured Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"[telegram] send failed: {e} — response: {e.response.text}")
        return False
    except Exception as e:
        print(f"[telegram] send failed: {e}")
        return False


def dispatch(filing: dict, summary: dict) -> bool:
    msg = format_message(filing, summary)
    return send_message(msg)
