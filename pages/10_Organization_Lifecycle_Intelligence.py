import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils.entity_selector import get_entity

st.set_page_config(
page_title="Lifecycle Intelligence",
page_icon="🔄",
layout="wide"
)

# ====================================

# ENTITY SELECTION

# ====================================

entity = get_entity()

entity_name = entity["Entity_Name"]

st.title("🔄 Organization Lifecycle Intelligence")

st.markdown(f"""

### Organizational Lifecycle Assessment

**Selected Entity:** {entity_name}

The Organizational Lifecycle Index (OLI) evaluates
the current maturity and strategic position of an entity.
""")

# ====================================

# ENTITY PROFILE

# ====================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
"Type",
entity["Entity_Type"]
)

c2.metric(
"Country",
entity["Country"]
)

c3.metric(
"Sector",
entity["Sector"]
)

c4.metric(
"Priority",
entity["Priority"]
)

st.divider()

# ====================================

# DEMO OLI ENGINE

# ====================================

entity_scores = {

```
"Tesla_Inc": 80,

"Microsoft_Corporation": 92,

"Kazan_Federal_University": 68,

"United_Nations_Childrens_Fund": 85,

"World_Health_Organization": 88
```

}

oli = entity_scores.get(
entity_name,
70
)

# ====================================

# CLASSIFICATION

# ====================================

if oli <= 20:

```
stage = "Startup"
```

elif oli <= 40:

```
stage = "Growth"
```

elif oli <= 60:

```
stage = "Maturity"
```

elif oli <= 75:

```
stage = "Recovery"
```

elif oli <= 90:

```
stage = "Leadership"
```

else:

```
stage = "Global Influence"
```

# ====================================

# KPI SECTION

# ====================================

k1, k2 = st.columns(2)

k1.metric(
"OLI Score",
oli
)

k2.metric(
"Lifecycle Stage",
stage
)

# ====================================

# OLI GAUGE

# ====================================

gauge = go.Figure(
go.Indicator(
mode="gauge+number",
value=oli,
title={
"text":
"Organizational Lifecycle Index"
},
gauge={
"axis": {
"range": [0, 100]
}
}
)
)

st.plotly_chart(
gauge,
use_container_width=True
)

# ====================================

# LIFECYCLE ROADMAP

# ====================================

st.subheader(
"Lifecycle Roadmap"
)

roadmap = pd.DataFrame({

```
"Stage": [

    "Startup",

    "Growth",

    "Maturity",

    "Recovery",

    "Leadership",

    "Global Influence"

],

"Position": [
    10,
    30,
    50,
    70,
    85,
    100
]
```

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

# ====================================

# FRAMEWORK

# ====================================

st.subheader(
"Lifecycle Framework"
)

framework = pd.DataFrame({

```
"Stage": [

    "Startup",

    "Growth",

    "Maturity",

    "Recovery",

    "Leadership",

    "Global Influence"

],

"Score Range": [

    "0-20",

    "21-40",

    "41-60",

    "61-75",

    "76-90",

    "91-100"

],

"Characteristics": [

    "Early visibility",

    "Rapid expansion",

    "Stable operations",

    "Repositioning phase",

    "Sector leadership",

    "Global influence"

]
```

})

st.dataframe(
framework,
use_container_width=True,
hide_index=True
)

# ====================================

# OLI DRIVERS

# ====================================

st.subheader(
"Future OLI Drivers"
)

drivers = pd.DataFrame({

```
"Driver": [

    "News Visibility",

    "Search Visibility",

    "Social Visibility",

    "Narrative Strength",

    "Reputation Resilience",

    "Financial Stability"

],

"Weight": [

    20,

    15,

    15,

    20,

    20,

    10

]
```

})

st.dataframe(
drivers,
use_container_width=True,
hide_index=True
)

# ====================================

# EXECUTIVE INSIGHT

# ====================================

st.subheader(
"Executive Insight"
)

st.info(
f"""
Entity: {entity_name}

```
OLI Score: {oli}

Lifecycle Stage: {stage}

Future versions will integrate:

• RII

• Google Trends Intelligence

• Social Media Intelligence

• Crisis Early Warning

• Narrative Intelligence

to calculate a dynamic Organizational Lifecycle Index.
"""
```

)
