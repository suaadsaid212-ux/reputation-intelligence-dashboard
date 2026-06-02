
import streamlit as st
import pandas as pd
import numpy as np
import feedparser
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

st.set_page_config(
    page_title="Sentiment & Subjectivity",
    layout="wide"
)

st.title("Sentiment & Subjectivity Intelligence")

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

    for entry in feed.entries[:25]:

        headline = entry.title

        vader_score = analyzer.polarity_scores(
            headline
        )["compound"]

        blob = TextBlob(headline)

        subjectivity = blob.sentiment.subjectivity

        polarity = blob.sentiment.polarity

        rows.append({
            "Company": company,
            "Headline": headline,
            "VADER Polarity": round(float(vader_score), 3),
            "TextBlob Polarity": round(float(polarity), 3),
            "Subjectivity": round(float(subjectivity), 3)
        })

df = pd.DataFrame(rows)

if df.empty:
    st.error("No sentiment data available.")
    st.stop()

st.subheader("Sentiment and Subjectivity Dataset")

st.dataframe(
    df,
    use_container_width=True
)

summary_df = (
    df.groupby("Company")
    .agg({
        "VADER Polarity": "mean",
        "TextBlob Polarity": "mean",
        "Subjectivity": "mean"
    })
    .reset_index()
)

st.subheader("Company-Level Sentiment and Subjectivity Summary")

st.dataframe(
    summary_df,
    use_container_width=True
)

st.subheader("Average Subjectivity by Company")

subjectivity_fig = go.Figure()

subjectivity_fig.add_trace(
    go.Bar(
        x=summary_df["Company"],
        y=summary_df["Subjectivity"],
        text=summary_df["Subjectivity"],
        textposition="auto"
    )
)

subjectivity_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    subjectivity_fig,
    use_container_width=True
)

st.subheader("Polarity vs Subjectivity Map")

scatter_fig = go.Figure()

for company in companies:

    company_df = df[
        df["Company"] == company
    ]

    scatter_fig.add_trace(
        go.Scatter(
            x=company_df["VADER Polarity"],
            y=company_df["Subjectivity"],
            mode="markers",
            name=company,
            text=company_df["Headline"],
            hovertemplate=
            "<b>%{text}</b><br>" +
            "Polarity: %{x}<br>" +
            "Subjectivity: %{y}<extra></extra>"
        )
    )

scatter_fig.update_layout(
    xaxis_title="Polarity",
    yaxis_title="Subjectivity",
    template="plotly_dark",
    height=600
)

st.plotly_chart(
    scatter_fig,
    use_container_width=True
)

st.subheader("High Subjectivity Narratives")

high_subjectivity_df = df[
    df["Subjectivity"] >= 0.6
]

if high_subjectivity_df.empty:
    st.info("No highly subjective narratives detected.")
else:
    st.dataframe(
        high_subjectivity_df.sort_values(
            by="Subjectivity",
            ascending=False
        ),
        use_container_width=True
    )
