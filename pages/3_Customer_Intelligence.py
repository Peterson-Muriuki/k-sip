import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Customer Intelligence | K-SIP", layout="wide")
st.title("Module 3 — Customer Intelligence Engine")
st.caption("PAYG segment economics · LTV/CAC analysis · Churn early signals · Pricing strategy")
st.divider()

if "payg_df" not in st.session_state:
    from utils.data_generator import generate_payg_customers
    st.session_state.payg_df = generate_payg_customers()

df = st.session_state.payg_df.copy()

tab1, tab2, tab3, tab4 = st.tabs(["Segment economics", "LTV / CAC modeler", "Churn signals", "Pricing strategy"])

with tab1:
    st.subheader("Customer segment unit economics")

    seg_stats = df.groupby("segment").agg(
        customers=("customer_id","count"),
        avg_payment_rate=("payment_rate","mean"),
        avg_ltv=("ltv_ksh","mean"),
        avg_cac=("cac_ksh","mean"),
        avg_net_econ=("net_unit_economics","mean"),
        churn_rate=("churned","mean"),
    ).reset_index()
    seg_stats["ltv_cac"] = (seg_stats["avg_ltv"] / seg_stats["avg_cac"]).round(2)
    seg_stats["avg_payment_rate"] = (seg_stats["avg_payment_rate"] * 100).round(1)
    seg_stats["churn_rate"] = (seg_stats["churn_rate"] * 100).round(1)
    seg_stats["avg_ltv"] = seg_stats["avg_ltv"].round(0)
    seg_stats["avg_cac"] = seg_stats["avg_cac"].round(0)
    seg_stats["avg_net_econ"] = seg_stats["avg_net_econ"].round(0)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(seg_stats, x="segment", y="avg_net_econ", color="avg_net_econ",
            color_continuous_scale=["#e74c3c","#f39c12","#2ecc71"],
            labels={"segment":"Segment","avg_net_econ":"Avg net unit economics (KES)"},
            title="Net unit economics by segment")
        fig.update_layout(height=320, margin=dict(l=0,r=0,t=40,b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True, key="seg_net_econ")

    with c2:
        fig2 = px.scatter(seg_stats, x="churn_rate", y="ltv_cac", size="customers",
            color="segment", text="segment",
            labels={"churn_rate":"Churn rate %","ltv_cac":"LTV/CAC ratio"},
            title="Churn vs LTV efficiency by segment")
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=320, margin=dict(l=0,r=0,t=40,b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True, key="seg_churn_ltv")

    st.dataframe(seg_stats.rename(columns={
        "segment":"Segment","customers":"Customers","avg_payment_rate":"Avg Payment Rate %",
        "avg_ltv":"Avg LTV (KES)","avg_cac":"Avg CAC (KES)","avg_net_econ":"Net Unit Econ (KES)",
        "churn_rate":"Churn Rate %","ltv_cac":"LTV/CAC"
    }), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("LTV / CAC modeler")
    st.caption("Adjust assumptions to model unit economics impact")

    c1, c2, c3 = st.columns(3)
    with c1:
        price_adj = st.slider("Product price adjustment %", -20, 20, 0, step=1, key="price_adj")
        cac_adj = st.slider("CAC adjustment %", -30, 30, 0, step=1, key="cac_adj")
    with c2:
        payment_rate_adj = st.slider("Payment rate improvement pp", -10, 20, 0, step=1, key="pr_adj")
        segment_filter = st.selectbox("Focus segment", ["All"] + df["segment"].unique().tolist(), key="seg_sel")
    with c3:
        product_filter = st.selectbox("Focus product", ["All"] + df["product"].unique().tolist(), key="prod_sel")

    filtered = df.copy()
    if segment_filter != "All":
        filtered = filtered[filtered["segment"] == segment_filter]
    if product_filter != "All":
        filtered = filtered[filtered["product"] == product_filter]

    base_ltv = filtered["ltv_ksh"].mean()
    base_cac = filtered["cac_ksh"].mean()
    base_ratio = base_ltv / base_cac

    adj_payment_rate = filtered["payment_rate"] + payment_rate_adj / 100
    adj_ltv = filtered["product_price"] * (1 + price_adj/100) * adj_payment_rate
    adj_cac = filtered["cac_ksh"] * (1 + cac_adj/100)
    new_ltv = adj_ltv.mean()
    new_cac = adj_cac.mean()
    new_ratio = new_ltv / new_cac

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Base LTV", f"KES {base_ltv:,.0f}")
    m2.metric("Modeled LTV", f"KES {new_ltv:,.0f}", f"{(new_ltv-base_ltv)/base_ltv*100:+.1f}%")
    m3.metric("Modeled CAC", f"KES {new_cac:,.0f}", f"{(new_cac-base_cac)/base_cac*100:+.1f}%")
    m4.metric("LTV/CAC Ratio", f"{new_ratio:.2f}x", f"{new_ratio-base_ratio:+.2f}x vs base")

    monthly = pd.DataFrame({
        "Month": range(1, 25),
        "Cumulative LTV (base)": [base_ltv * m/24 for m in range(1, 25)],
        "Cumulative LTV (modeled)": [new_ltv * m/24 for m in range(1, 25)],
        "CAC (base)": [base_cac]*24,
        "CAC (modeled)": [new_cac]*24,
    })
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Cumulative LTV (base)"], name="LTV base", line=dict(color="#95a5a6", dash="dot")))
    fig3.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Cumulative LTV (modeled)"], name="LTV modeled", line=dict(color="#2ecc71", width=2.5)))
    fig3.add_trace(go.Scatter(x=monthly["Month"], y=monthly["CAC (base)"], name="CAC base", line=dict(color="#e74c3c", dash="dot")))
    fig3.add_trace(go.Scatter(x=monthly["Month"], y=monthly["CAC (modeled)"], name="CAC modeled", line=dict(color="#e74c3c", width=2.5)))
    fig3.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
        xaxis_title="Month", yaxis_title="KES",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True, key="ltv_cac_curve")

with tab3:
    st.subheader("Churn prediction & early signals")

    features = ["payment_rate","tenure_days","missed_payments","days_overdue","product_price","cac_ksh"]
    X = df[features]
    y = df["churned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingClassifier(n_estimators=80, max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    df["churn_score"] = model.predict_proba(X[features])[:, 1]

    fi = pd.DataFrame({"Feature": features, "Importance": model.feature_importances_}).sort_values("Importance", ascending=True)

    c1, c2 = st.columns(2)
    with c1:
        fig4 = px.bar(fi, x="Importance", y="Feature", orientation="h",
            color="Importance", color_continuous_scale=["#3498db","#e74c3c"],
            title="Churn drivers — feature importance")
        fig4.update_layout(height=300, margin=dict(l=0,r=0,t=40,b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True, key="churn_feat_imp")

    with c2:
        risk_bands = pd.cut(df["churn_score"], bins=[0,0.3,0.6,1.0], labels=["Low (<30%)","Medium (30-60%)","High (>60%)"])
        band_counts = risk_bands.value_counts().reset_index()
        band_counts.columns = ["Risk Band","Count"]
        fig5 = px.pie(band_counts, names="Risk Band", values="Count",
            color="Risk Band",
            color_discrete_map={"Low (<30%)":"#2ecc71","Medium (30-60%)":"#f39c12","High (>60%)":"#e74c3c"},
            title="Portfolio churn risk distribution")
        fig5.update_layout(height=300, margin=dict(l=0,r=0,t=40,b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True, key="churn_pie")

    st.subheader("High-risk accounts — intervention list")
    at_risk = df[df["churn_score"] > 0.6].sort_values("churn_score", ascending=False).head(20).copy()
    at_risk["churn_score"] = at_risk["churn_score"].round(3)
    at_risk["payment_rate"] = at_risk["payment_rate"].round(3)

    def color_churn(val):
        if val > 0.8:
            return "background-color: #ffd5d5"
        elif val > 0.6:
            return "background-color: #fff3cd"
        return ""

    display = at_risk[["customer_id","county","segment","product","payment_rate","days_overdue","churn_score"]].rename(columns={
        "customer_id":"Customer ID","county":"County","segment":"Segment","product":"Product",
        "payment_rate":"Payment Rate","days_overdue":"Days Overdue","churn_score":"Churn Score"
    })
    st.dataframe(
        display.style.applymap(color_churn, subset=["Churn Score"]),
        use_container_width=True, hide_index=True
    )

with tab4:
    st.subheader("Pricing sensitivity analysis")
    st.caption("Model revenue impact of price changes across segments")

    price_range = np.arange(0.7, 1.31, 0.05)
    elasticity_by_segment = {"Low income": -1.8, "Lower middle": -1.3, "Middle": -0.9, "Upper middle": -0.5}
    base_revenue = df.groupby("segment")["total_paid_ksh"].sum()

    rows = []
    for multiplier in price_range:
        for seg, elasticity in elasticity_by_segment.items():
            demand_change = max(0.1, 1 + elasticity * (multiplier - 1))
            rev = base_revenue.get(seg, 0) * multiplier * demand_change
            rows.append({"Price multiplier": round(multiplier, 2), "Segment": seg, "Modeled revenue": round(rev, 0)})

    price_df = pd.DataFrame(rows)
    fig6 = px.line(price_df, x="Price multiplier", y="Modeled revenue", color="Segment",
        labels={"Price multiplier":"Price vs base (1.0 = current)", "Modeled revenue":"Modeled revenue (KES)"},
        title="Revenue sensitivity to price — by segment")
    fig6.add_vline(x=1.0, line_dash="dash", line_color="gray", annotation_text="Current price")
    fig6.update_layout(height=380, margin=dict(l=0,r=0,t=40,b=0),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig6, use_container_width=True, key="pricing_sensitivity")