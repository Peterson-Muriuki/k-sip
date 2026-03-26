import streamlit as st

st.set_page_config(
    page_title="K-SIP | Kenya Strategic Intelligence Platform",
    page_icon="assets/favicon.txt",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stSidebar"] { background: #0f1117; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
.metric-card { background: #1e2130; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.5rem; }
.alert-high { border-left: 4px solid #e74c3c; padding-left: 10px; margin: 6px 0; }
.alert-med  { border-left: 4px solid #f39c12; padding-left: 10px; margin: 6px 0; }
.alert-low  { border-left: 4px solid #2ecc71; padding-left: 10px; margin: 6px 0; }
</style>
""", unsafe_allow_html=True)

st.title("K-SIP — Kenya Strategic Intelligence Platform")
st.markdown("#### Peterson Muriuki · Business Intelligence Portfolio Project")
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### Module 1")
    st.info("**Early Warning System**\nMacro + regulatory signals, EA fintech risk index, inflection alerts")

with col2:
    st.markdown("### Module 2")
    st.warning("**Competitive War Room**\nCompetitor profiles, scenario simulation, whitespace map")

with col3:
    st.markdown("### Module 3")
    st.success("**Customer Intelligence**\nPAYG segments, LTV/CAC, churn signals, pricing strategy")

with col4:
    st.markdown("### Module 4")
    st.error("**Diagnostics Board**\nLeading indicators, variance root cause, action recommendations")

st.divider()
st.markdown("**Navigate using the sidebar.** Each module feeds into the AI Strategy Brief on the home page.")
st.divider()

from utils.data_generator import generate_payg_customers, generate_macro_signals, generate_competitor_profiles, generate_regulatory_events
from utils.ai_synthesis import generate_strategic_brief
import pandas as pd

if "payg_df" not in st.session_state:
    with st.spinner("Loading platform data..."):
        st.session_state.payg_df = generate_payg_customers()
        st.session_state.macro_df = generate_macro_signals()
        st.session_state.competitors_df = generate_competitor_profiles()
        st.session_state.regulatory_df = generate_regulatory_events()

payg_df = st.session_state.payg_df
macro_df = st.session_state.macro_df
competitors_df = st.session_state.competitors_df
regulatory_df = st.session_state.regulatory_df

latest = macro_df.iloc[-1]
risk_index = float(latest["risk_index"])
churn_rate = float(payg_df["churned"].mean())
ltv_cac = float((payg_df["ltv_ksh"] / payg_df["cac_ksh"]).mean())
top_segment = payg_df.groupby("segment")["net_unit_economics"].mean().idxmax()

c1, c2, c3, c4 = st.columns(4)
c1.metric("EA Fintech Risk Index", f"{risk_index:.1f}/100", delta=f"{risk_index - 60:.1f} vs threshold")
c2.metric("Portfolio Churn Rate", f"{churn_rate:.1%}", delta=f"{churn_rate - 0.25:.1%} vs 25% target", delta_color="inverse")
c3.metric("LTV / CAC Ratio", f"{ltv_cac:.2f}x", delta=f"{ltv_cac - 3.0:.2f} vs 3.0x target")
c4.metric("Active Competitors Tracked", str(len(competitors_df)))

st.divider()
st.subheader("AI Strategic Brief")

top_alerts = regulatory_df.sort_values("date", ascending=False)["event"].tolist()
competitor_moves = competitors_df["recent_move"].tolist()

if st.button("Generate / Refresh AI Brief"):
    with st.spinner("Synthesising intelligence signals..."):
        brief = generate_strategic_brief(
            risk_index, top_alerts, competitor_moves, churn_rate, ltv_cac, top_segment
        )
        st.session_state.brief = brief

if "brief" in st.session_state:
    st.markdown(st.session_state.brief)
else:
    st.info("Click **Generate / Refresh AI Brief** to synthesise all platform signals into an executive recommendation.")