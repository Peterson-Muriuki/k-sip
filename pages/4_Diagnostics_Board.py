import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Diagnostics Board | K-SIP", layout="wide")
st.title("Module 4 — Strategic Performance Diagnostics Board")
st.caption("Leading indicators · Variance root cause · Action recommendations")
st.divider()

if "payg_df" not in st.session_state:
    from utils.data_generator import generate_payg_customers
    st.session_state.payg_df = generate_payg_customers()
if "macro_df" not in st.session_state:
    from utils.data_generator import generate_macro_signals
    st.session_state.macro_df = generate_macro_signals()

df = st.session_state.payg_df
macro = st.session_state.macro_df

targets = {
    "Collections rate %":       (df["payment_rate"].mean() * 100,          82.0,  False),
    "Churn rate %":             (df["churned"].mean() * 100,                25.0,  True),
    "LTV/CAC ratio":            ((df["ltv_ksh"] / df["cac_ksh"]).mean(),    3.0,   False),
    "Avg days overdue":         (df["days_overdue"].mean(),                 12.0,  True),
    "Net unit economics (KES)": (df["net_unit_economics"].mean(),           8000.0,False),
}

from utils.ai_synthesis import generate_variance_explanation

st.subheader("KPI diagnostics — actual vs target")

for idx, (kpi, (actual, target, is_inverse)) in enumerate(targets.items()):
    pct_var = (actual - target) / target * 100
    healthy = (pct_var >= 0 and not is_inverse) or (pct_var < 0 and is_inverse)

    col1, col2, col3 = st.columns([2, 1, 3])
    with col1:
        delta_val = f"{pct_var:+.1f}% vs target"
        if "ratio" in kpi:
            display_val = f"{actual:.2f}"
        elif "KES" in kpi:
            display_val = f"KES {actual:,.0f}"
        else:
            display_val = f"{actual:.1f}{'%' if '%' in kpi else ''}"
        st.metric(kpi, display_val, delta_val,
            delta_color="normal" if healthy else "inverse")

    with col2:
        pct_of_target = min(actual / target, 1.5) if target > 0 else 0
        bar_color = "#2ecc71" if healthy else "#e74c3c"
        fig = go.Figure(go.Bar(
            x=[pct_of_target], y=[""], orientation="h",
            marker_color=bar_color, width=0.4
        ))
        fig.add_vline(x=1.0, line_color="gray", line_dash="dash")
        fig.update_layout(
            height=60, margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(range=[0, 1.5], showticklabels=False),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"kpi_bar_{idx}")

    with col3:
        if not healthy:
            diagnosis_key = f"diag_{kpi}"
            if diagnosis_key not in st.session_state:
                if st.button("Diagnose", key=f"btn_diag_{idx}"):
                    context = f"Risk index: {macro.iloc[-1]['risk_index']:.1f}, CBK rate: {macro.iloc[-1]['cbk_rate_pct']:.2f}%, inflation: {macro.iloc[-1]['inflation_pct']:.1f}%"
                    with st.spinner("Running AI diagnosis..."):
                        diag = generate_variance_explanation(kpi, actual, target, pct_var, context)
                        st.session_state[diagnosis_key] = diag
            if diagnosis_key in st.session_state:
                st.info(st.session_state[diagnosis_key])
        else:
            st.success(f"On track — {pct_var:+.1f}% vs target")

st.divider()
st.subheader("Leading indicator trends — 24 months")

col_a, col_b = st.columns(2)
with col_a:
    fig_mm = px.line(macro, x="month", y="mobile_money_vol_bn",
        title="Mobile money volume (leading indicator for PAYG demand)",
        labels={"mobile_money_vol_bn":"Volume (KES Bn)","month":"Month"})
    fig_mm.update_layout(height=260, margin=dict(l=0,r=0,t=40,b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_mm, use_container_width=True, key="lead_mobile_money")

with col_b:
    fig_cg = px.line(macro, x="month", y="credit_growth_pct",
        title="Credit growth % (leading indicator for repayment capacity)",
        labels={"credit_growth_pct":"Credit growth %","month":"Month"})
    fig_cg.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Health threshold")
    fig_cg.update_layout(height=260, margin=dict(l=0,r=0,t=40,b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_cg, use_container_width=True, key="lead_credit_growth")

st.divider()
st.subheader("Recommended actions — this week")

actions = [
    {"priority":"HIGH",   "kpi":"Churn rate %",             "action":"Launch proactive rescheduling outreach for accounts with churn score > 0.6 (see Module 3 intervention list)","owner":"Customer Success","timeline":"7 days"},
    {"priority":"HIGH",   "kpi":"Collections rate %",        "action":"Segment collections messaging by risk band — Low income needs flexible windows, not penalty messages",        "owner":"Collections + Product","timeline":"14 days"},
    {"priority":"MEDIUM", "kpi":"LTV/CAC ratio",             "action":"Model impact of solar duty removal on hardware cost — present pricing headroom analysis to board",            "owner":"Finance + BI","timeline":"21 days"},
    {"priority":"MEDIUM", "kpi":"Net unit economics (KES)",  "action":"Upper middle segment has strongest unit economics — review acquisition budget allocation vs Low income",      "owner":"Marketing + Finance","timeline":"30 days"},
    {"priority":"LOW",    "kpi":"Avg days overdue",          "action":"Submit PAYG repayment history to CRB pilot as per new CBK regulation — build customer credit identity",      "owner":"Compliance + Data","timeline":"60 days"},
]

priority_icons = {"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}
actions_df = pd.DataFrame(actions)
actions_df["priority"] = actions_df["priority"].apply(lambda x: f"{priority_icons.get(x,'')} {x}")
st.dataframe(actions_df.rename(columns={
    "priority":"Priority","kpi":"KPI","action":"Recommended Action","owner":"Owner","timeline":"Timeline"
}), use_container_width=True, hide_index=True)