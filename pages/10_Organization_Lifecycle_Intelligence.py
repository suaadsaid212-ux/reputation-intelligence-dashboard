import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.entity_selector import get_entity

st.set_page_config(
page_title="Lifecycle Intelligence",
page_icon="🔄",
layout="wide"
)

entity = get_entity()

entity_name = entity["Entity_Name"]

st.title("🔄 Organization Lifecycle Intelligence")

st.markdown(f"""

### Organizational Lifecycle Assessment

**Selected Entity:** {entity_name}

The Organizational Lifecycle Index (OLI) evaluates
the current maturity and strategic position of an entity.
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Type", entity["Entity_Type"])
c2.metric("Country", entity["Country"])
c3.metric("Sector", entity["Sector"])
c4.metric("Priority", entity["Priority"])

st.divider()

entity_scores = {
"Tesla_Inc": 80,
"Microsoft_Corporation": 92,
"Kazan_Federal_University": 68,
"United_Nations_Childrens_Fund": 85,
"World_Health_Organization": 88
}

oli = entity_scores.get(
entity_name,
70
)

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

k1, k2 = st.columns(2)

k1.metric("OLI Score", oli)
k2.metric("Lifecycle Stage", stage)

gauge = go.Figure(
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
gauge,
use_container_width=True
)

st.subheader("Lifecycle Roadmap")

roadmap = pd.DataFrame({
"Stage": [
"Startup",
"Growth",
"Maturity",
"Recovery",
"Leadership",
"Global Influence"
],
"Position": [10, 30, 50, 70, 85, 100]
})

roadmap_fig = go.Figure()

roadmap_fig.add_trace(
go.Scatter(
x=roadmap["Position"],
y=roadmap["Stage"],
mode="lines+markers"
)
)

roadmap_fig.update_layout(
height=500,
xaxis_title="Lifecycle Progress",
yaxis_title="Stage"
)

st.plotly_chart(
roadmap_fig,
use_container_width=True
)

st.subheader("Executive Insight")

st.info(
f"""
Entity: {entity_name}

OLI Score: {oli}

Lifecycle Stage: {stage}

Future versions will integrate:

• RII

• Google Trends Intelligence

• Social Media Intelligence

• Crisis Early Warning

• Narrative Intelligence
"""
)
