
import streamlit as st
import pandas as pd
import numpy as np
import feedparser
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

st.set_page_config(
    page_title="NRRI Risk Index",
    layout="wide"
)

st.title("NRRI Risk Index")

st.write(
    "NRRI stands for Narrative Reputation Risk Index. "
    "It combines narrative volume, sentiment volatility, subjectivity, "
    "negative impact, and counter-narrative strength."
)

company_input = st.sidebar.text_input(
    "Enter company tickers",
    "TSLA,MSFT,META"
)

companies = [
    c.strip().upper()
    for c in company_input.split(",")
    if c.strip() != ""
]

analyzer = SentimentIntensityAnalyzer()

rows = []

for company in companies:

    rss_url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(rss_url)

    headlines = []
    scores = []
    subjectivities = []

    for entry in feed.entries[:25]:

        headline = entry.title

        vader_score = analyzer.polarity_scores(
            headline
        )["compound"]

        subjectivity = TextBlob(
            headline
        ).sentiment.subjectivity

        headlines.append(headline)
        scores.append(vader_score)
        subjectivities.append(subjectivity)

    if len(scores) == 0:
        continue

    narrative_volume = len(headlines) / 25

    sentiment_volatility = np.std(scores)

    negative_impact = (
        len([s for s in scores if s <= -0.3])
        / len(scores)
    )

    subjectivity_score = np.mean(subjectivities)

    counter_narrative = (
        len([s for s in scores if s >= 0.3])
        / len(scores)
    )

    narrative_complexity = (
        np.std([len(h) for h in headlines])
        / 100
    )

    NRRI = (
        (0.20 * narrative_volume) +
        (0.25 * sentiment_volatility) +
        (0.20 * negative_impact) +
        (0.15 * subjectivity_score) +
        (0.10 * narrative_complexity) -
        (0.10 * counter_narrative)
    )

    NRRI_100 = NRRI * 100

    if NRRI_100 >= 70:
        risk_level = "Critical"
    elif NRRI_100 >= 50:
        risk_level = "High"
    elif NRRI_100 >= 30:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    rows.append({
        "Company": company,
        "Narrative Volume": round(float(narrative_volume), 3),
        "Sentiment Volatility": round(float(sentiment_volatility), 3),
        "Negative Impact": round(float(negative_impact), 3),
        "Subjectivity": round(float(subjectivity_score), 3),
        "Narrative Complexity": round(float(narrative_complexity), 3),
        "Counter-Narrative": round(float(counter_narrative), 3),
        "NRRI": round(float(NRRI_100), 2),
        "Risk Level": risk_level
    })

nrri_df = pd.DataFrame(rows)

if nrri_df.empty:
    st.error("No NRRI data available.")
    st.stop()

st.subheader("NRRI Results")

st.dataframe(
    nrri_df,
    use_container_width=True
)

st.subheader("NRRI Ranking")

ranking_df = nrri_df.sort_values(
    by="NRRI",
    ascending=False
)

ranking_fig = go.Figure()

ranking_fig.add_trace(
    go.Bar(
        x=ranking_df["Company"],
        y=ranking_df["NRRI"],
        text=ranking_df["NRRI"],
        textposition="auto"
    )
)

ranking_fig.update_layout(
    title="Narrative Reputation Risk Index by Company",
    xaxis_title="Company",
    yaxis_title="NRRI Score",
    template="plotly_dark",
    height=550
)

st.plotly_chart(
    ranking_fig,
    use_container_width=True
)

st.subheader("NRRI Component Heatmap")

component_matrix = nrri_df[
    [
        "Narrative Volume",
        "Sentiment Volatility",
        "Negative Impact",
        "Subjectivity",
        "Narrative Complexity",
        "Counter-Narrative"
    ]
]

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=component_matrix.values,
        x=component_matrix.columns,
        y=nrri_df["Company"],
        colorscale="Reds"
    )
)

heatmap_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    heatmap_fig,
    use_container_width=True
)

st.subheader("NRRI Interpretation")

for _, row in ranking_df.iterrows():

    company = row["Company"]
    score = row["NRRI"]
    level = row["Risk Level"]

    if level == "Critical":
        st.error(
            f"{company}: Critical NRRI level. The organization shows severe narrative reputation exposure."
        )
    elif level == "High":
        st.warning(
            f"{company}: High NRRI level. The organization shows strong negative narrative pressure."
        )
    elif level == "Moderate":
        st.info(
            f"{company}: Moderate NRRI level. The organization shows observable but manageable narrative risk."
        )
    else:
        st.success(
            f"{company}: Low NRRI level. The organization shows relatively stable narrative conditions."
        )
