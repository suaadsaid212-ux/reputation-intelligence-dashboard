import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

from utils.entity_selector import get_entity

st.set_page_config(
page_title="Crisis Early Warning",
page_icon="🚨",
layout="wide"
)

entity = get_entity()

entity_name = entity["Entity_Name"]

st.title("🚨 Crisis Early Warning")

st.markdown(f"""

### Crisis Monitoring & Early Detection

**Selected Entity:** {entity_name}

This module identifies emerging reputation threats,
narrative escalation, search spikes, and social pressure.
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Type", entity["Entity_Type"])
c2.metric("Country", entity["Country"])
c3.metric("Sector", entity["Sector"])
c4.metric("Priority", entity["Priority"])

st.divider()

random.seed(42)

news_risk = random.randint(20, 90)
social_risk = random.randint(20, 90)
search_risk = random.randint(20, 90)
rii_risk = random.randint(20, 90)
oli_risk = random.randint(20, 90)

crisis_score = round(
(
news_risk
+ social_risk
+ search_risk
+ rii_risk
+ oli_risk
) / 5,
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
# KPI SECTION
# ====================================

st.subheader(
    "Executive Risk Overview"
)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("News Risk", news_risk)
k2.metric("Social Risk", social_risk)
k3.metric("Search Risk", search_risk)
k4.metric("RII Risk", rii_risk)
k5.metric("OLI Risk", oli_risk)

st.success(
    f"Current Alert Level: {level}"
)

# ====================================
# CRISIS GAUGE
# ====================================

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=crisis_score,
        title={"text": "Crisis Risk Score"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    )
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

# ====================================
# RISK BREAKDOWN
# ====================================

st.subheader(
    "Risk Breakdown"
)

risk_df = pd.DataFrame({
    "Risk Source": [
        "News",
        "Social",
        "Search",
        "RII",
        "OLI"
    ],
    "Score": [
        news_risk,
        social_risk,
        search_risk,
        rii_risk,
        oli_risk
    ]
})

bar_fig = go.Figure()

bar_fig.add_trace(
    go.Bar(
        x=risk_df["Risk Source"],
        y=risk_df["Score"],
        text=risk_df["Score"],
        textposition="auto"
    )
)

bar_fig.update_layout(
    height=500,
    yaxis_title="Risk Score"
)

st.plotly_chart(
    bar_fig,
    use_container_width=True
)

# ====================================
# CRISIS MATRIX
# ====================================

st.subheader(
    "Threat Matrix"
)

matrix_df = pd.DataFrame({
    "Threat": [
        "Negative News",
        "Search Spike",
        "Social Backlash",
        "Narrative Escalation",
        "Reputation Decline"
    ],
    "Probability": [
        random.randint(30, 100),
        random.randint(30, 100),
        random.randint(30, 100),
        random.randint(30, 100),
        random.randint(30, 100)
    ]
})

st.dataframe(
    matrix_df,
    use_container_width=True,
    hide_index=True
)

# ====================================
# RECOMMENDED ACTIONS
# ====================================

st.subheader(
    "Recommended Actions"
)

if crisis_score > 80:

    st.error(
        """
Immediate action required.

• Activate crisis response team

• Increase media monitoring

• Prepare stakeholder response

• Review narrative escalation
"""
    )

elif crisis_score > 60:

    st.warning(
        """
Elevated monitoring recommended.

• Monitor social sentiment

• Review search activity

• Track news developments
"""
    )

else:

    st.info(
        """
Situation currently stable.

Continue standard monitoring.
"""
    )

st.info(
f"""
Entity: {entity_name}

Crisis Score: {crisis_score}

Alert Level: {level}

Current model integrates:

• News Intelligence

• Social Intelligence

• Search Intelligence

• RII

• OLI

Future versions will connect directly to:

• Google Trends

• Social Media APIs

• News Monitoring

• Reputation Forecasting
"""
)
