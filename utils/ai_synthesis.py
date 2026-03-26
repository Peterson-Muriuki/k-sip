import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def _call_ollama(prompt, max_tokens=600):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": 0.7}
        }, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        return None
    except Exception as e:
        return None


def generate_strategic_brief(risk_index, top_alerts, competitor_moves, churn_rate, ltv_cac_ratio, top_segment):
    prompt = f"""You are the Business Intelligence Manager for M-KOPA Kenya, a leading PAYG solar and fintech company.
Based on the following intelligence signals, generate a concise executive strategic brief (max 350 words).

SIGNALS:
- EA Fintech Risk Index: {risk_index}/100 (above 60 = elevated)
- Top regulatory/macro alerts: {'; '.join(top_alerts[:3])}
- Recent competitor moves: {'; '.join(competitor_moves[:2])}
- Portfolio churn rate: {churn_rate:.1%}
- LTV/CAC ratio: {ltv_cac_ratio:.2f}x
- Strongest customer segment: {top_segment}

FORMAT your brief with exactly these sections:
1. SITUATION (2 sentences)
2. TOP THREATS (2 bullet points)
3. TOP OPPORTUNITIES (2 bullet points)
4. RECOMMENDED ACTIONS (3 specific actions with owner and timeline)
5. WATCH LIST (1 thing to monitor next 30 days)

Be specific to Kenya fintech context. Be direct."""

    result = _call_ollama(prompt, 700)
    if result:
        return result
    return _mock_brief(risk_index, top_alerts, churn_rate)


def generate_competitor_narrative(competitor_name, profile_data, scenario):
    prompt = f"""You are a competitive intelligence analyst for M-KOPA Kenya.
Competitor: {competitor_name}
Profile: {profile_data}
Scenario: {scenario}

In 150 words describe:
1. How {competitor_name} would likely respond in this scenario
2. Their biggest vulnerability M-KOPA could exploit
3. One pre-emptive action M-KOPA should take now

Be direct and specific to Kenya PAYG/fintech context."""

    result = _call_ollama(prompt, 300)
    if result:
        return result
    return f"""**{competitor_name} — War-game analysis (demo mode)**

In this scenario ({scenario}), {competitor_name} would likely focus on defending their core customer base through pricing adjustments and accelerated collections activity. Their primary vulnerability lies in their {profile_data.get('vulnerability', 'operational constraints')}, which M-KOPA can exploit by moving faster on customer retention.

**Pre-emptive action:** Lock in your highest-value customers in affected segments with proactive rescheduling offers before {competitor_name} pivots their sales team toward the same accounts.

[Connect Ollama + Mistral locally to enable live AI narratives — run: ollama pull mistral]"""


def generate_variance_explanation(metric_name, actual, target, pct_variance, context_data):
    prompt = f"""You are a BI analyst at M-KOPA Kenya. A key metric has deviated from target.
Metric: {metric_name}
Actual: {actual}
Target: {target}
Variance: {pct_variance:+.1f}%
Context: {context_data}

In 80 words: state the most likely root cause, one contributing factor, and one recommended action.
Be specific to Kenya fintech/PAYG context. No hedging."""

    result = _call_ollama(prompt, 150)
    if result:
        return result

    direction = "below" if pct_variance < 0 else "above"
    return f"Variance of {pct_variance:+.1f}% {direction} target. Most likely driven by macro headwinds visible in the current risk index. Recommend reviewing segment-level breakdown to isolate whether this is concentrated in low-income counties or spread across the portfolio. [Connect Ollama + Mistral for AI diagnosis]"


def _mock_brief(risk_index, top_alerts, churn_rate):
    level = "elevated" if risk_index > 60 else "moderate"
    return f"""**SITUATION**
The EA fintech risk environment is currently {level} (index: {risk_index:.1f}/100). CBK rate tightening and KES depreciation are compressing consumer disposable income and creating PAYG collections headwinds across low-income segments.

**TOP THREATS**
- Rising cost of credit reducing PAYG down payment capacity in low-income segments
- Regulatory compliance burden creating asymmetric cost pressure on smaller players

**TOP OPPORTUNITIES**
- CBR reform enabling alternative data for credit scoring — PAYG repayment history now credit-relevant
- Solar import duty reduction (0% off-grid) creates ~10% hardware cost headroom

**RECOMMENDED ACTIONS**
1. Collections: Launch proactive rescheduling for accounts with churn score >0.6 — Customer Success, 30 days
2. Product: Model pricing impact of hardware cost reduction — Finance + Product, 45 days
3. Credit: Submit PAYG repayment data to CRB pilot — Compliance + Data, 60 days

**WATCH LIST**
Monitor CBK MPC decision next 30 days — a rate hold or cut would significantly improve collections outlook.

---
*Demo mode — install Ollama and run `ollama pull mistral` for live AI briefs*"""