import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Social Media Intelligence",
    layout="wide"
)

st.title("📱 Social Media Intelligence")

st.markdown("""
Monitor social reputation signals across digital platforms.

Current Version:
- YouTube
- Reddit

Future Versions:
- X (Twitter)
- LinkedIn
- TikTok
- Facebook
""")

# ====================================
# ORGANIZATION INPUT
# ====================================

organization = st.sidebar.text_input(
    "Organization",
    "Tesla"
)

# ====================================
# DEMO DATA
# Replace later with APIs
# ====================================

youtube_mentions = np.random.randint(500, 3000)
reddit_mentions = np.random.randint(100, 1500)

youtube_sentiment = np.random.uniform(-1, 1)
reddit_sentiment = np.random.uniform(-1, 1)

youtube_engagement = np.random.randint(10000, 100000)
reddit_engagement = np.random.randint(1000, 20000)

# ====================================
# CALCULATED SCORES
# ====================================

ssi = round(
    (
        (youtube_sentiment + 1) * 50 +
        (reddit_sentiment + 1) * 50
    ) / 2,
    2
)

svi = round(
    min(
        100,
        (
            youtube_mentions +
            reddit_mentions
        ) / 40
    ),
    2
)

ses = round(
    min(
        100,
        (
            youtube_engagement +
            reddit_engagement
        ) / 1000
    ),
    2
)

npi = round(
    max(
        0,
        100 - ssi
    ),
    2
)

srs = round(
    (
        0.30 * ssi +
        0.25 * npi +
        0.25 * svi +
        0.20 * ses
    ),
    2
)

# ====================================
# RISK CLASSIFICATION
# ====================================

if srs <= 20:
    risk = "Stable"

elif srs <= 40:
    risk = "Monitor"

elif srs <= 60:
    risk = "Elevated"

elif srs <= 80:
    risk = "High Risk"

else:
    risk = "Critical"

# ====================================
# EXECUTIVE KPIs
# ====================================

st.subheader("Executive Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("SSI", ssi)
c2.metric("SVI", svi)
c3.metric("NPI", npi)
c4.metric("SRS", srs)

st.success(f"Current Social Risk Status: {risk}")

# ====================================
# PLATFORM COMPARISON
# ====================================

st.subheader("Platform Comparison")

platform_df = pd.DataFrame({
    "Platform": ["YouTube", "Reddit"],
    "Mentions": [
        youtube_mentions,
        reddit_mentions
    ],
    "Engagement": [
        youtube_engagement,
        reddit_engagement
    ]
})

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=platform_df["Platform"],
        y=platform_df["Mentions"],
        name="Mentions"
    )
)

fig.add_trace(
    go.Bar(
        x=platform_df["Platform"],
        y=platform_df["Engagement"],
        name="Engagement"
    )
)

fig.update_layout(
    template="plotly_dark",
    barmode="group",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================
# SENTIMENT DONUT
# ====================================

st.subheader("Social Sentiment")

positive = max(
    0,
    round(ssi)
)

negative = max(
    0,
    round(npi)
)

neutral = max(
    0,
    100 - positive - negative
)

donut = go.Figure(
    data=[
        go.Pie(
            labels=[
                "Positive",
                "Neutral",
                "Negative"
            ],
            values=[
                positive,
                neutral,
                negative
            ],
            hole=0.6
        )
    ]
)

donut.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    donut,
    use_container_width=True
)

# ====================================
# SOCIAL RISK GAUGE
# ====================================

st.subheader("Social Risk Score")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=srs,
        title={"text": "SRS"},
        gauge={
            "axis": {
                "range": [0, 100]
            }
        }
    )
)

gauge.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

# ====================================
# NARRATIVE INTELLIGENCE
# ====================================

st.subheader("Trending Narratives")

narratives = pd.DataFrame({
    "Topic": [
        "Innovation",
        "Leadership",
        "AI",
        "Sustainability",
        "Market Growth"
    ],
    "Frequency": [
        89,
        76,
        64,
        52,
        40
    ]
})

st.dataframe(
    narratives,
    use_container_width=True
)

# ====================================
# EXECUTIVE INSIGHT
# ====================================

st.subheader("Executive Insight")

st.info(
    f"""
    {organization} currently shows a Social Risk Score of {srs}.

    Visibility Score: {svi}

    Sentiment Score: {ssi}

    Narrative Pressure: {npi}

    Current Classification: {risk}

    These metrics will feed directly into:
    - RII
    - NRRI
    - Crisis Early Warning
    - Lifecycle Intelligence
    """
)
