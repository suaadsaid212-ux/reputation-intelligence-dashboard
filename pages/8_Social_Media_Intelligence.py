import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from utils.entity_selector import get_entity

st.set_page_config(
    page_title="Social Media Intelligence",
    page_icon="📱",
    layout="wide",
)

entity = get_entity()
organization = entity["Entity_Name"]

st.title("📱 Social Media Intelligence")

st.markdown(f"""
### Monitoring Social Reputation Signals

**Selected Entity:** {organization}

Sources:

- YouTube
- Reddit

Future Sources:

- X (Twitter)
- LinkedIn
- TikTok
- Facebook
""")

np.random.seed(42)

youtube_mentions = np.random.randint(500, 3000)
reddit_mentions = np.random.randint(100, 1500)

youtube_sentiment = np.random.uniform(-1, 1)
reddit_sentiment = np.random.uniform(-1, 1)

youtube_engagement = np.random.randint(10000, 100000)
reddit_engagement = np.random.randint(1000, 20000)

ssi = round(
    (
        (youtube_sentiment + 1) * 50
        + (reddit_sentiment + 1) * 50
    ) / 2,
    2,
)

svi = round(
    min(
        100,
        (
            youtube_mentions
            + reddit_mentions
        ) / 40,
    ),
    2,
)

ses = round(
    min(
        100,
        (
            youtube_engagement
            + reddit_engagement
        ) / 1000,
    ),
    2,
)

npi = round(
    max(
        0,
        100 - ssi,
    ),
    2,
)

srs = round(
    (
        0.30 * ssi
        + 0.25 * npi
        + 0.25 * svi
        + 0.20 * ses
    ),
    2,
)

if srs <= 20:
    risk = "🟢 Stable"
elif srs <= 40:
    risk = "🟡 Monitor"
elif srs <= 60:
    risk = "🟠 Elevated"
elif srs <= 80:
    risk = "🔴 High Risk"
else:
    risk = "🚨 Critical"

st.subheader("Executive Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("SSI", ssi)
c2.metric("SVI", svi)
c3.metric("NPI", npi)
c4.metric("SRS", srs)

st.success(f"Current Social Risk Status: {risk}")

st.subheader("Platform Comparison")

platform_df = pd.DataFrame({
    "Platform": [
        "YouTube",
        "Reddit",
    ],
    "Mentions": [
        youtube_mentions,
        reddit_mentions,
    ],
    "Engagement": [
        youtube_engagement,
        reddit_engagement,
    ],
})

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=platform_df["Platform"],
        y=platform_df["Mentions"],
        name="Mentions",
    )
)

fig.add_trace(
    go.Bar(
        x=platform_df["Platform"],
        y=platform_df["Engagement"],
        name="Engagement",
    )
)

fig.update_layout(
    barmode="group",
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Social Sentiment")

    positive = round(ssi)
    negative = round(npi)
    neutral = max(
        0,
        100 - positive - negative,
    )

    donut = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Positive",
                    "Neutral",
                    "Negative",
                ],
                values=[
                    positive,
                    neutral,
                    negative,
                ],
                hole=0.6,
            )
        ]
    )

    st.plotly_chart(donut, use_container_width=True)

with col2:
    st.subheader("Social Risk Score")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=srs,
            title={"text": "SRS"},
            gauge={
                "axis": {
                    "range": [0, 100],
                },
            },
        )
    )

    st.plotly_chart(gauge, use_container_width=True)

st.subheader("Trending Narratives")

narratives = pd.DataFrame({
    "Topic": [
        "Innovation",
        "Leadership",
        "AI",
        "Sustainability",
        "Growth",
    ],
    "Frequency": [
        89,
        76,
        64,
        52,
        40,
    ],
})

st.dataframe(narratives, use_container_width=True)

st.subheader("Entity Information")

st.write(f"**Type:** {entity['Entity_Type']}")
st.write(f"**Country:** {entity['Country']}")
st.write(f"**Sector:** {entity['Sector']}")

st.subheader("Executive Insight")

st.info(f"""
{organization} currently has a Social Risk Score of {srs}.

Social Sentiment Index (SSI): {ssi}

Social Visibility Index (SVI): {svi}

Narrative Pressure Index (NPI): {npi}

Current Classification: {risk}

These indicators feed directly into:

- Reputation Intelligence Index (RII)
- Narrative Reputation Risk Index (NRRI)
- Organizational Lifecycle Index (OLI)
- Crisis Early Warning System
""")
