import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import feedparser
import plotly.graph_objects as go

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from utils.entity_selector import get_entity

st.set_page_config(
page_title="RII Reputation Intelligence Index",
page_icon="🏆",
layout="wide"
)

# ====================================

# ENTITY SELECTION

# ====================================

entity = get_entity()

entity_name = entity["Entity_Name"]
entity_type = entity["Entity_Type"]
ticker = str(entity["Ticker"])

st.title("🏆 Reputation Intelligence Index (RII)")

st.markdown(f"""

### Reputation Risk Assessment

**Selected Entity:** {entity_name}

RII measures organizational reputation risk using:

• Exposure

• Vulnerability

• Resilience
""")

# ====================================

# ENTITY PROFILE

# ====================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Type", entity["Entity_Type"])
c2.metric("Country", entity["Country"])
c3.metric("Sector", entity["Sector"])
c4.metric("Priority", entity["Priority"])

st.divider()

# ====================================

# SETTINGS

# ====================================

start_date = st.sidebar.selectbox(
"Analysis Period",
[
"2025-01-01",
"2024-01-01",
"2023-01-01",
"2021-01-01"
]
)

analyzer = SentimentIntensityAnalyzer()

# ====================================

# NEWS DATA

# ====================================

feed = feedparser.parse(
f"https://news.google.com/rss/search?q={entity_name}"
)

headlines = []
sentiment_scores = []
subjectivity_scores = []

for entry in feed.entries[:25]:

```
headline = entry.title

sentiment = analyzer.polarity_scores(
    headline
)["compound"]

subjectivity = TextBlob(
    headline
).sentiment.subjectivity

headlines.append(headline)

sentiment_scores.append(
    sentiment
)

subjectivity_scores.append(
    subjectivity
)
```

if len(sentiment_scores) == 0:

```
st.warning(
    "No news data found."
)

st.stop()
```

# ====================================

# FINANCIAL VOLATILITY

# ====================================

financial_volatility = 0

if (
entity_type == "Company"
and
ticker != ""
and
ticker != "nan"
):

```
try:

    stock = yf.download(
        ticker,
        start=start_date,
        progress=False,
        auto_adjust=True
    )

    if not stock.empty:

        stock["Returns"] = (
            stock["Close"]
            .pct_change()
        )

        financial_volatility = (
            stock["Returns"]
            .std()
        )

except:

    financial_volatility = 0
```

# ====================================

# RII COMPONENTS

# ====================================

news_volume = len(headlines)

negative_ratio = len(
[
s
for s in sentiment_scores
if s <= -0.3
]
) / len(sentiment_scores)

positive_ratio = len(
[
s
for s in sentiment_scores
if s >= 0.3
]
) / len(sentiment_scores)

sentiment_volatility = np.std(
sentiment_scores
)

avg_subjectivity = np.mean(
subjectivity_scores
)

exposure_score = min(
100,
(news_volume / 25) * 100
)

vulnerability_score = min(
100,
(
negative_ratio * 40
+
sentiment_volatility * 30
+
avg_subjectivity * 20
+
financial_volatility * 100
)
)

resilience_score = min(
100,
(
positive_ratio * 50
+
(1 - sentiment_volatility) * 30
+
(1 - negative_ratio) * 20
)
)

rii = (
0.35 * exposure_score
+
0.35 * vulnerability_score
-
0.30 * resilience_score
)

rii = max(
0,
min(100, rii)
)

# ====================================

# STATUS

# ====================================

if rii >= 81:
status = "🚨 Crisis Zone"

elif rii >= 61:
status = "🔴 High Risk"

elif rii >= 41:
status = "🟠 Vulnerable"

elif rii >= 21:
status = "🟡 Monitor"

else:
status = "🟢 Stable"

# ====================================

# KPI SECTION

# ====================================

st.subheader(
"Executive Reputation KPIs"
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
"Exposure",
round(exposure_score, 2)
)

k2.metric(
"Vulnerability",
round(vulnerability_score, 2)
)

k3.metric(
"Resilience",
round(resilience_score, 2)
)

k4.metric(
"RII",
round(rii, 2)
)

st.success(
f"Current Status: {status}"
)

# ====================================

# GAUGE

# ====================================

fig = go.Figure(
go.Indicator(
mode="gauge+number",
value=rii,
title={
"text":
"Reputation Intelligence Index"
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

# RADAR

# ====================================

st.subheader(
"RII Component Radar"
)

radar = go.Figure()

radar.add_trace(
go.Scatterpolar(
r=[
exposure_score,
vulnerability_score,
resilience_score,
rii
],
theta=[
"Exposure",
"Vulnerability",
"Resilience",
"RII"
],
fill="toself",
name=entity_name
)
)

radar.update_layout(
polar=dict(
radialaxis=dict(
visible=True,
range=[0, 100]
)
),
height=600
)

st.plotly_chart(
radar,
use_container_width=True
)

# ====================================

# HEADLINES

# ====================================

st.subheader(
"Latest News Headlines"
)

headline_df = pd.DataFrame({
"Headline": headlines
})

st.dataframe(
headline_df,
use_container_width=True
)

# ====================================

# INTERPRETATION

# ====================================

st.subheader(
"Executive Interpretation"
)

st.info(
f"""
Entity: {entity_name}

```
RII Score: {round(rii,2)}

Status: {status}

Exposure Score:
{round(exposure_score,2)}

Vulnerability Score:
{round(vulnerability_score,2)}

Resilience Score:
{round(resilience_score,2)}

This score feeds directly into:

• Organizational Lifecycle Intelligence

• Crisis Early Warning

• Reputation Forecasting

• Global Risk Monitoring
"""
```

)
