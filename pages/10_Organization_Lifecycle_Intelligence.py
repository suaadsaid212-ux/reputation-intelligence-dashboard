import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Lifecycle Intelligence",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 Organization Lifecycle Intelligence")

st.markdown("""
The Organizational Lifecycle Index (OLI) estimates
the current lifecycle stage of an entity.
""")

# ====================================
# LOAD REGISTRY
# ====================================

df = pd.read_csv(
    "config/entity_registry.csv",
    encoding="utf-8-sig"
)

# ====================================
# ENTITY SELECTION
# ====================================

entity = st.selectbox(
    "Select Entity",
    df["Entity_Name"]
)

# ====================================
# DEMO OLI SCORE
# ====================================

entity_scores = {
    "Tesla_Inc": 80,
    "Microsoft_Corporation": 90,
    "Kazan_Federal_University": 65,
    "United_Nations_Childrens_Fund": 85,
    "World_Health_Organization": 88
}

oli = entity_scores.get(entity, 70)

# ====================================
# CLASSIFICATION
# ====================================

if oli <= 20:
    stage = "Startup"

elif oli <= 40:
    stage = "Growth"

elif oli <= 60:
    stage = "Maturity"

elif oli <= 75:
    stage = "Recovery"

elif oli <= 90:
    stage = "Leadership"

else:
    stage = "Global Influence"

# ====================================
# KPI
# ====================================

col1, col2 = st.columns(2)

col1.metric(
    "OLI Score",
    oli
)

col2.metric(
    "Lifecycle Stage",
    stage
)

# ====================================
# GAUGE
# ====================================

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=oli,
        title={"text": "Organizational Lifecycle Index"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================
# STAGES
# ====================================

st.subheader("Lifecycle Framework")

st.info(
    """
    0–20     Startup

    21–40    Growth

    41–60    Maturity

    61–75    Recovery

    76–90    Leadership

    91–100   Global Influence
    """
)

# ====================================
# FUTURE VERSION
# ====================================

st.subheader("Future Data Inputs")

st.markdown(
    """
    Future versions will calculate OLI using:

    - News Visibility
    - Search Visibility
    - Social Visibility
    - Financial Growth
    - Narrative Strength
    - Reputation Resilience

    instead of fixed demo scores.
    """
)
