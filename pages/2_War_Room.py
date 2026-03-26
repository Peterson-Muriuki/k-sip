import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="War Room | K-SIP", layout="wide")
st.title("Module 2 — Competitive War Room")
st.caption("Competitor profiles · Scenario simulation · Strategic whitespace map")
st.divider()

if "competitors_df" not in st.session_state:
    from utils.data_generator import generate_competitor_profiles
    st.session_state.competitors_df = generate_competitor_profiles()

df = st.session_state.competitors_df

tab1, tab2, tab3 = st.tabs(["Competitor profiles", "Scenario war-game", "Whitespace map"])

with tab1:
    st.subheader("Competitor landscape — Kenya PAYG & fintech")

    col_l, col_r = st.columns([2, 1])
    with col_l:
        fig = px.scatter(
            df, x="est_customers", y="churn_est_pct",
            size="avg_price_ksh", color="type",
            hover_name="name", text="name",
            labels={"est_customers": "Est. active customers", "churn_est_pct": "Estimated churn %", "avg_price_ksh": "Avg price (KES)"},
            color_discrete_map={"Solar PAYG": "#3498db", "Mobile lending": "#e74c3c"}
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(
            height=380, margin=dict(l=0, r=0, t=20, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        selected = st.selectbox("View competitor profile", df["name"].tolist())
        row = df[df["name"] == selected].iloc[0]
        st.markdown(f"**Type:** {row['type']}")
        st.markdown(f"**Est. customers:** {row['est_customers']:,}")
        st.markdown(f"**Counties active:** {row['counties']}")
        st.markdown(f"**Avg price:** KES {row['avg_price_ksh']:,}")
        st.markdown(f"**Financing term:** {row['financing_months']} months")
        st.markdown(f"**Est. churn:** {row['churn_est_pct']}%")
        st.divider()
        st.markdown(f"**Recent move:** {row['recent_move']}")
        st.markdown(f"**Vulnerability:** {row['vulnerability']}")
        st.markdown(f"**Strategic intent:** {row['strategic_intent']}")

    st.divider()
    st.subheader("Competitor scorecard")
    display_cols = ["name","type","est_customers","avg_price_ksh","churn_est_pct","strategic_intent"]
    st.dataframe(df[display_cols].rename(columns={
        "name":"Competitor","type":"Type","est_customers":"Est. Customers",
        "avg_price_ksh":"Avg Price (KES)","churn_est_pct":"Churn Est. %",
        "strategic_intent":"Strategic Intent"
    }), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Scenario war-game simulator")

    scenarios = [
        "CBK raises rates again by 100bps — consumer credit squeeze intensifies",
        "Solar import duties removed entirely — hardware costs drop 20%",
        "Safaricom launches PAYG solar product bundled with M-PESA",
        "New regulation requires all PAYG providers to report to CRB",
        "Global funding drought — Series B rounds dry up for EA startups",
        "Kenya GDP growth slows to 3% — rural purchasing power drops",
    ]

    selected_scenario = st.selectbox("Select scenario to war-game", scenarios)
    selected_competitor = st.selectbox("War-game against which competitor?", df["name"].tolist())

    if st.button("Run war-game analysis"):
        from utils.ai_synthesis import generate_competitor_narrative
        comp_row = df[df["name"] == selected_competitor].iloc[0].to_dict()
        with st.spinner(f"Analysing {selected_competitor} response to scenario..."):
            narrative = generate_competitor_narrative(selected_competitor, comp_row, selected_scenario)
        st.session_state.war_game_result = narrative
        st.session_state.war_game_scenario = selected_scenario
        st.session_state.war_game_competitor = selected_competitor

    if "war_game_result" in st.session_state:
        st.markdown(f"**Scenario:** {st.session_state.war_game_scenario}")
        st.markdown(f"**Competitor:** {st.session_state.war_game_competitor}")
        st.divider()
        st.markdown(st.session_state.war_game_result)

with tab3:
    st.subheader("Strategic whitespace map — Kenya counties")
    st.caption("Underserved segments by geography — bubble size = estimated addressable market")

    whitespace_data = pd.DataFrame([
        {"county":"Turkana","segment":"Low income","payg_penetration_pct":4,"addressable_hh":85000,"competitors_active":1},
        {"county":"Garissa","segment":"Low income","payg_penetration_pct":3,"addressable_hh":62000,"competitors_active":1},
        {"county":"Wajir","segment":"Low income","payg_penetration_pct":2,"addressable_hh":48000,"competitors_active":0},
        {"county":"Isiolo","segment":"Lower middle","payg_penetration_pct":8,"addressable_hh":28000,"competitors_active":2},
        {"county":"Marsabit","segment":"Low income","payg_penetration_pct":3,"addressable_hh":35000,"competitors_active":1},
        {"county":"Tana River","segment":"Low income","payg_penetration_pct":5,"addressable_hh":41000,"competitors_active":1},
        {"county":"Kwale","segment":"Lower middle","payg_penetration_pct":12,"addressable_hh":55000,"competitors_active":2},
        {"county":"Kilifi","segment":"Lower middle","payg_penetration_pct":15,"addressable_hh":72000,"competitors_active":3},
        {"county":"Lamu","segment":"Lower middle","payg_penetration_pct":9,"addressable_hh":18000,"competitors_active":1},
        {"county":"Homa Bay","segment":"Low income","payg_penetration_pct":11,"addressable_hh":88000,"competitors_active":2},
        {"county":"Migori","segment":"Lower middle","payg_penetration_pct":13,"addressable_hh":76000,"competitors_active":2},
        {"county":"Bungoma","segment":"Lower middle","payg_penetration_pct":16,"addressable_hh":92000,"competitors_active":3},
    ])

    fig = px.scatter(
        whitespace_data, x="payg_penetration_pct", y="addressable_hh",
        size="addressable_hh", color="competitors_active",
        hover_name="county", text="county",
        labels={"payg_penetration_pct":"PAYG penetration %","addressable_hh":"Addressable households","competitors_active":"Competitors active"},
        color_continuous_scale="RdYlGn_r",
        title="Low penetration + large market = highest whitespace priority"
    )
    fig.update_traces(textposition="top center")
    fig.add_vline(x=10, line_dash="dash", line_color="gray", annotation_text="10% penetration threshold")
    fig.update_layout(
        height=420, margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Top whitespace opportunities (bottom-left quadrant):**")
    top_ws = whitespace_data[whitespace_data["payg_penetration_pct"] < 10].sort_values("addressable_hh", ascending=False)
    st.dataframe(top_ws[["county","segment","payg_penetration_pct","addressable_hh","competitors_active"]].rename(columns={
        "county":"County","segment":"Segment","payg_penetration_pct":"Penetration %",
        "addressable_hh":"Addressable HH","competitors_active":"Competitors"
    }), use_container_width=True, hide_index=True)