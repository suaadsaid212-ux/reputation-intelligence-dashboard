import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="Crisis Early Warning",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Crisis Early Warning")

st.markdown("""
Early detection system for reputation threats,
negative narratives, and emerging crises.
""")

# ====================================
# LOAD REGISTRY
# ====================================

df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)

entity = st.selectbox(
    "Select Entity",
    df["Entity_Name"]
)

# ====================================
# DEMO SCORES
# ====================================

news_risk = random.randint(20, 90)
social_risk = random.randint(20, 90)
search_risk = random.randint(20, 90)

crisis_score = round(
    (
        news_risk +
        social_risk +
        search_risk
    ) / 3,
    2
)

# ====================================
# ALERT LEVEL
# ====================================

if crisis_score <= 20:
    level = "🟢 Normal"

elif crisis_score <= 40:
    level = "🟡 Watch"

elif crisis_score <= 60:
    level = "🟠 Elevated"

elif crisis_score <= 80:
    level = "🔴 High Risk"

else:
    level = "🚨 Crisis Alert"

# ====================================
# KPI CARDS
# ====================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "News Risk",
    news_risk
)

c2.metric(
    "Social Risk",
    social_risk
)

c3.metric(
    "Search Risk",
    search_risk
)

c4.metric(
    "Crisis Score",
    crisis_score
)

st.success(
    f"Current Alert Level: {level}"
)

# ====================================
# GAUGE
# ====================================

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=crisis_score,
        title={
            "text":
            "Crisis Risk Score"
        },
        gauge={
            "axis": {
                "range": [0, 100]
            }
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================
# RISK BREAKDOWN
# ====================================

risk_df = pd.DataFrame({
    "Risk Source": [
        "News",
        "Social",
        "Search"
    ],
    "Score": [
        news_risk,
        social_risk,
        search_risk
    ]
})

st.subheader("Risk Breakdown")

st.bar_chart(
    risk_df.set_index(
        "Risk Source"
    )
)

# ====================================
# RECOMMENDATIONS
# ====================================

st.subheader(
    "Recommended Actions"
)

if crisis_score > 80:

    st.error(
        """
        Immediate response required.

        • Activate crisis team
        • Increase monitoring
        • Prepare response strategy
        """
    )

elif crisis_score > 60:

    st.warning(
        """
        Elevated monitoring recommended.

        • Track narratives
        • Monitor social sentiment
        """
    )

else:

    st.info(
        """
        Situation stable.

        Continue routine monitoring.
        """
    )
