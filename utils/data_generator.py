import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_payg_customers(n=1200, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    counties = [
        "Nairobi","Mombasa","Kisumu","Nakuru","Eldoret",
        "Machakos","Meru","Nyeri","Kakamega","Kisii",
        "Garissa","Isiolo","Turkana","Wajir","Mandera"
    ]
    county_weights = [
        0.18,0.10,0.09,0.08,0.07,
        0.06,0.05,0.05,0.05,0.05,
        0.04,0.04,0.04,0.05,0.05
    ]
    products = ["Solar Home S200","Solar Home S350","Solar TV Bundle","Solar Pump","EV Swap"]
    product_prices = {"Solar Home S200":18000,"Solar Home S350":28000,"Solar TV Bundle":35000,"Solar Pump":55000,"EV Swap":85000}
    segments = ["Low income","Lower middle","Middle","Upper middle"]
    seg_weights = [0.40, 0.35, 0.18, 0.07]

    start_date = datetime(2022, 1, 1)

    records = []
    for i in range(n):
        county = random.choices(counties, county_weights)[0]
        segment = random.choices(segments, seg_weights)[0]
        product = random.choices(products, weights=[0.30,0.25,0.20,0.15,0.10])[0]
        price = product_prices[product]

        tenure_days = np.random.randint(30, 900)
        activation_date = start_date + timedelta(days=np.random.randint(0, 700))

        if segment == "Low income":
            base_payment_rate = np.random.beta(2, 5)
        elif segment == "Lower middle":
            base_payment_rate = np.random.beta(3, 4)
        elif segment == "Middle":
            base_payment_rate = np.random.beta(5, 3)
        else:
            base_payment_rate = np.random.beta(7, 2)

        missed_payments = int((1 - base_payment_rate) * tenure_days / 30)
        total_paid = round(price * base_payment_rate * (tenure_days / 730), 2)

        days_overdue = max(0, int(np.random.exponential(15) * (1 - base_payment_rate)))

        churned = 1 if (base_payment_rate < 0.35 and tenure_days > 90) else 0
        churn_prob = round(1 - base_payment_rate, 3)

        ltv = round(price * base_payment_rate, 2)
        cac = round(np.random.normal(2800, 400), 2)

        records.append({
            "customer_id": f"KE{str(i+1).zfill(5)}",
            "county": county,
            "segment": segment,
            "product": product,
            "product_price": price,
            "activation_date": activation_date.strftime("%Y-%m-%d"),
            "tenure_days": tenure_days,
            "payment_rate": round(base_payment_rate, 3),
            "total_paid_ksh": total_paid,
            "missed_payments": missed_payments,
            "days_overdue": days_overdue,
            "churned": churned,
            "churn_probability": churn_prob,
            "ltv_ksh": ltv,
            "cac_ksh": cac,
            "net_unit_economics": round(ltv - cac, 2),
        })

    return pd.DataFrame(records)


def generate_macro_signals():
    months = pd.date_range("2023-01-01", periods=24, freq="MS")
    np.random.seed(7)
    data = {
        "month": months,
        "kes_usd": np.round(np.linspace(122, 158, 24) + np.random.normal(0, 2, 24), 2),
        "inflation_pct": np.round(np.linspace(9.1, 5.8, 24) + np.random.normal(0, 0.4, 24), 2),
        "cbk_rate_pct": np.round(np.linspace(8.75, 13.0, 24) + np.random.normal(0, 0.1, 24), 2),
        "mobile_money_vol_bn": np.round(np.linspace(540, 720, 24) + np.random.normal(0, 15, 24), 1),
        "credit_growth_pct": np.round(np.linspace(12.5, 7.2, 24) + np.random.normal(0, 0.8, 24), 2),
        "fintech_funding_usd_mn": np.round(np.abs(np.random.normal(45, 30, 24)), 1),
    }
    df = pd.DataFrame(data)
    df["risk_index"] = np.round(
        (df["kes_usd"] / 160 * 25) +
        (df["inflation_pct"] / 10 * 25) +
        (df["cbk_rate_pct"] / 15 * 25) +
        ((100 - df["credit_growth_pct"]) / 100 * 25), 1
    )
    return df


def generate_competitor_profiles():
    return pd.DataFrame([
        {"name":"Sunculture","type":"Solar PAYG","est_customers":180000,"counties":12,"avg_price_ksh":45000,"financing_months":24,"churn_est_pct":28,"recent_move":"Raised $14M Series B, expanding North Rift","vulnerability":"High price point, limited urban play","strategic_intent":"Rural dominance, crop-linked financing"},
        {"name":"d.light","type":"Solar PAYG","est_customers":320000,"counties":18,"avg_price_ksh":22000,"financing_months":18,"churn_est_pct":32,"recent_move":"Launched D20 tablet bundle","vulnerability":"Hardware margin squeeze","strategic_intent":"Volume play, entry-level"},
        {"name":"Solar Now","type":"Solar PAYG","est_customers":95000,"counties":8,"avg_price_ksh":38000,"financing_months":36,"churn_est_pct":22,"recent_move":"Partnered with equity bank for co-financing","vulnerability":"Bank dependency, slow approval","strategic_intent":"Premium segment, long tenure"},
        {"name":"Tala","type":"Mobile lending","est_customers":4000000,"counties":47,"avg_price_ksh":5000,"financing_months":1,"churn_est_pct":45,"recent_move":"Launched Tala savings product","vulnerability":"Rising NPLs, regulatory pressure","strategic_intent":"Financial super-app pivot"},
        {"name":"KCB M-Pesa","type":"Mobile lending","est_customers":6500000,"counties":47,"avg_price_ksh":8000,"financing_months":3,"churn_est_pct":38,"recent_move":"Reduced Fuliza rates post-CBK pressure","vulnerability":"Margin compression","strategic_intent":"Ecosystem lock-in via Safaricom"},
    ])


def generate_regulatory_events():
    return pd.DataFrame([
        {"date":"2024-01-15","body":"CBK","event":"Digital Credit Provider licensing deadline extended","impact":"Medium","category":"Regulatory","strategic_implication":"3-month window for unlicensed players to comply — monitor Tala, Carbon"},
        {"date":"2024-02-20","body":"CBK","event":"CBK raises base rate to 13.0%","impact":"High","category":"Macro","strategic_implication":"Consumer disposable income squeeze — expect PAYG collections stress Q2"},
        {"date":"2024-03-05","body":"CA Kenya","event":"New data localisation requirements for fintech","impact":"Medium","category":"Regulatory","strategic_implication":"Raises compliance cost for foreign-backed competitors"},
        {"date":"2024-04-12","body":"EPRA","event":"Solar import duty revised — 0% for off-grid systems","impact":"High","category":"Policy","strategic_implication":"Hardware cost reduction of est. 8-12% — pricing headroom for PAYG players"},
        {"date":"2024-05-28","body":"CBK","event":"Mobile money transaction limits raised","impact":"Medium","category":"Policy","strategic_implication":"Enables larger PAYG down payments via M-PESA — reduce default risk"},
        {"date":"2024-07-01","body":"KRA","event":"Digital service tax expanded to PAYG platforms","impact":"High","category":"Tax","strategic_implication":"Margin impact ~1.5% — smaller players most affected"},
        {"date":"2024-08-14","body":"CBK","event":"Credit Reference Bureau reform — alternative data allowed","impact":"High","category":"Regulatory","strategic_implication":"Major opportunity — PAYG repayment history now counts toward credit score"},
        {"date":"2024-10-03","body":"National Treasury","event":"Budget allocates KES 3B to last-mile electrification","impact":"Medium","category":"Policy","strategic_implication":"Tailwind for solar home systems in off-grid counties"},
    ])