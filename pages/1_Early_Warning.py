import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Early Warning | K-SIP", layout="wide")
st.title("Module 1 — Early Warning System")
st.caption("EA Fintech Risk Index · Macro signals · Regulatory event tracker")
st.divider()

if "macro_df" not in st.session_state:
    from utils.data_generator import generate_macro_signals, generate_regulatory_events
    st.session_state.macro_df = generate_macro_signals()
    st.session_state.regulatory_df = generate_regulatory_events()

macro_df = st.session_state.macro_df
reg_df = st.session_state.regulatory_df

latest = macro_df.iloc[-1]
prev = macro_df.iloc[-2]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Risk Index", f"{latest['risk_index']:.1f}", f"{latest['risk_index']-prev['risk_index']:+.1f}")
c2.metric("KES/USD", f"{latest['kes_usd']:.1f}", f"{latest['kes_usd']-prev['kes_usd']:+.1f}", delta_color="inverse")
c3.metric("Inflation %", f"{latest['inflation_pct']:.1f}%", f"{latest['inflation_pct']-prev['inflation_pct']:+.1f}%", delta_color="inverse")
c4.metric("CBK Rate %", f"{latest['cbk_rate_pct']:.2f}%", f"{latest['cbk_rate_pct']-prev['cbk_rate_pct']:+.2f}%", delta_color="inverse")
c5.metric("Mobile Money Vol (Bn)", f"KES {latest['mobile_money_vol_bn']:.0f}B", f"{latest['mobile_money_vol_bn']-prev['mobile_money_vol_bn']:+.1f}")

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("EA Fintech Risk Index — 24 months")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=macro_df["month"], y=macro_df["risk_index"],
        mode="lines+markers", name="Risk Index",
        line=dict(color="#e74c3c", width=2.5),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.08)"
    ))
    fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Alert threshold (60)")
    fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="Critical threshold (75)")
    fig.update_layout(
        height=320, margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title=None, yaxis_title="Risk Index (0-100)",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Key macro indicators")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=macro_df["month"], y=macro_df["kes_usd"], name="KES/USD", line=dict(color="#3498db")))
    fig2.add_trace(go.Scatter(x=macro_df["month"], y=macro_df["inflation_pct"]*10, name="Inflation % (×10)", line=dict(color="#e67e22", dash="dot")))
    fig2.add_trace(go.Scatter(x=macro_df["month"], y=macro_df["cbk_rate_pct"]*8, name="CBK Rate % (×8)", line=dict(color="#9b59b6", dash="dash")))
    fig2.update_layout(
        height=280, margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.subheader("Regulatory event tracker")
    reg_df_sorted = reg_df.sort_values("date", ascending=False)
    for _, row in reg_df_sorted.iterrows():
        impact_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(row["impact"], "⚪")
        with st.expander(f"{impact_color} {row['date']} · {row['body']}"):
            st.markdown(f"**Event:** {row['event']}")
            st.markdown(f"**Strategic implication:** {row['strategic_implication']}")
            st.markdown(f"**Category:** `{row['category']}` · **Impact:** `{row['impact']}`")

st.divider()
st.subheader("Signal decomposition — what's driving the risk index?")

components = {
    "KES depreciation": float(latest["kes_usd"]) / 160 * 25,
    "Inflation pressure": float(latest["inflation_pct"]) / 10 * 25,
    "Credit tightening": float(latest["cbk_rate_pct"]) / 15 * 25,
    "Credit growth slowdown": (100 - float(latest["credit_growth_pct"])) / 100 * 25,
}
fig3 = px.bar(
    x=list(components.keys()), y=list(components.values()),
    labels={"x": "Signal", "y": "Contribution to Risk Index"},
    color=list(components.values()),
    color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"]
)
fig3.update_layout(
    height=280, margin=dict(l=0, r=0, t=10, b=0),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False
)
st.plotly_chart(fig3, use_container_width=True)