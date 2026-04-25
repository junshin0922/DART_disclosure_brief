import json
import anthropic
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Filing types too routine/noisy to summarize
_SKIP_PATTERNS = [
    "투자설명서",
    "일괄신고추가서류",
    "증권발행실적보고서",
    "기업설명회(IR)개최",
    "공정거래자율준수프로그램",
    "약관에의한금융거래",
]

SYSTEM_PROMPT = """\
You are a financial analyst assistant specializing in Korean corporate disclosures. \
You translate and summarize Korean DART filings for English-speaking institutional investors.

Rules:
- Be factual and precise. Preserve all numbers exactly as given.
- Do NOT give investment advice or buy/sell recommendations.
- If a number is labeled as preliminary (잠정), note it.
- Units: 백만원 = KRW millions. Convert to billions for readability (e.g., KRW 52,576B).
- Keep bullets tight: one fact per bullet, lead with the metric name.
- market_impact: one sentence max, neutral analytical tone.\
"""

USER_TEMPLATE = """\
Company: {corp_name}
Filing type: {report_nm}
Date: {rcept_dt}

--- DOCUMENT ---
{text}
--- END ---

Return JSON only:
{{
  "bullets": ["<fact 1>", "<fact 2>", "<fact 3>"],
  "market_impact": "<one sentence>"
}}
"""


def is_material(report_nm: str) -> bool:
    """Return False for routine/noisy filing types."""
    return not any(p in report_nm for p in _SKIP_PATTERNS)


def summarize(filing: dict, text: str) -> dict | None:
    """Call Claude Haiku and return {bullets, market_impact} or None on failure."""
    prompt = USER_TEMPLATE.format(
        corp_name=filing["corp_name"],
        report_nm=filing["report_nm"],
        rcept_dt=filing["rcept_dt"],
        text=text[:6000],  # cap to ~1500 tokens of context
    )

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as e:
        print(f"[summarizer] failed for {filing['rcept_no']}: {e}")
        return None
