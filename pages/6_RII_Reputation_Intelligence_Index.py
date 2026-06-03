import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import feedparser
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

st.set_page_config(
    page_title="RII Reputation Intelligence Index",
    layout="wide"
)

st.title("Reputation Intelligence Index (RII)")

st.write(
    "RII measures organizational reputation risk using three layers: "
    "Exposure, Vulnerability, and Resilience."
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

start_date = st.sidebar.selectbox(
    "Analysis Period",
    ["2025-01-01", "2024-01-01", "2023-01-01", "2021-01-01"]
)

analyzer = SentimentIntensityAnalyzer()

rows = []

for company in companies:

    feed = feedparser.parse(
        f"https://news.google.com/rss/search?q={company}"
    )

    headlines = []
    sentiment_scores = []
    subjectivity_scores = []

    for entry in feed.entries[:25]:

        headline = entry.title

        sentiment = analyzer.polarity_scores(
            headline
        )["compound"]

        subjectivity = TextBlob(
            headline
        ).sentiment.subjectivity

        headlines.append(headline)
        sentiment_scores.append(sentiment)
        subjectivity_scores.append(subjectivity)

    if len(sentiment_scores) == 0:
        continue

    stock = yf.download(
        company,
        start=start_date,
        progress=False,
        auto_adjust=True
    )

    if stock.empty:
        financial_volatility = 0
    else:
        stock["Returns"] = stock["Close"].pct_change()
        financial_volatility = stock["Returns"].std()

    news_volume = len(headlines)
    negative_ratio = len([s for s in sentiment_scores if s <= -0.3]) / len(sentiment_scores)
    positive_ratio = len([s for s in sentiment_scores if s >= 0.3]) / len(sentiment_scores)
    sentiment_volatility = np.std(sentiment_scores)
    avg_subjectivity = np.mean(subjectivity_scores)

    exposure_score = min(
        100,
        (news_volume / 25) * 100
    )

    vulnerability_score = min(
        100,
        (
            negative_ratio * 40
            + sentiment_volatility * 30
            + avg_subjectivity * 20
            + financial_volatility * 100
        )
    )

    resilience_score = min(
        100,
        (
            positive_ratio * 50
            + (1 - sentiment_volatility) * 30
            + (1 - negative_ratio) * 20
        )
    )

    rii = (
        0.35 * exposure_score
        + 0.35 * vulnerability_score
        - 0.30 * resilience_score
    )

    rii = max(0, min(100, rii))

    if rii >= 81:
        status = "Crisis Zone"
    elif rii >= 61:
        status = "High Risk"
    elif rii >= 41:
        status = "Vulnerable"
    elif rii >= 21:
        status = "Monitor"
    else:
        status = "Stable"

    rows.append({
        "Company": company,
        "Exposure Score": round(float(exposure_score), 2),
        "Vulnerability Score": round(float(vulnerability_score), 2),
        "Resilience Score": round(float(resilience_score), 2),
        "RII Score": round(float(rii), 2),
        "Status": status
    })

rii_df = pd.DataFrame(rows)

if rii_df.empty:
    st.error("No RII data available.")
    st.stop()

st.subheader("RII Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Exposure", round(rii_df["Exposure Score"].mean(), 2))
col2.metric("Average Vulnerability", round(rii_df["Vulnerability Score"].mean(), 2))
col3.metric("Average Resilience", round(rii_df["Resilience Score"].mean(), 2))
col4.metric("Average RII", round(rii_df["RII Score"].mean(), 2))

st.subheader("RII Results Table")

st.dataframe(
    rii_df.sort_values(
        by="RII Score",
        ascending=False
    ),
    use_container_width=True
)

st.subheader("RII Ranking")

rank_fig = go.Figure()

rank_fig.add_trace(
    go.Bar(
        x=rii_df["Company"],
        y=rii_df["RII Score"],
        text=rii_df["RII Score"],
        textposition="auto"
    )
)

rank_fig.update_layout(
    template="plotly_dark",
    height=500,
    yaxis_title="RII Score"
)

st.plotly_chart(
    rank_fig,
    use_container_width=True
)

st.subheader("Exposure, Vulnerability, and Resilience Radar")

radar_fig = go.Figure()

for _, row in rii_df.iterrows():

    radar_fig.add_trace(
        go.Scatterpolar(
            r=[
                row["Exposure Score"],
                row["Vulnerability Score"],
                row["Resilience Score"],
                row["RII Score"]
            ],
            theta=[
                "Exposure",
                "Vulnerability",
                "Resilience",
                "RII"
            ],
            fill="toself",
            name=row["Company"]
        )
    )

radar_fig.update_layout(
    template="plotly_dark",
    height=650,
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    )
)

st.plotly_chart(
    radar_fig,
    use_container_width=True
)

st.subheader("RII Component Heatmap")

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=rii_df[
            [
                "Exposure Score",
                "Vulnerability Score",
                "Resilience Score",
                "RII Score"
            ]
        ].values,
        x=[
            "Exposure",
            "Vulnerability",
            "Resilience",
            "RII"
        ],
        y=rii_df["Company"],
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

st.subheader("Executive RII Interpretation")

for _, row in rii_df.iterrows():

    company = row["Company"]
    rii = row["RII Score"]
    status = row["Status"]
    exposure = row["Exposure Score"]
    vulnerability = row["Vulnerability Score"]
    resilience = row["Resilience Score"]

    if status == "Crisis Zone":
        st.error(
            f"{company} is in the Crisis Zone. Exposure and vulnerability are very high, "
            f"while resilience is not sufficient to absorb reputational pressure."
        )
    elif status == "High Risk":
        st.warning(
            f"{company} is classified as High Risk. The organization shows strong visibility "
            f"and elevated vulnerability."
        )
    elif status == "Vulnerable":
        st.info(
            f"{company} is Vulnerable. Reputation conditions should be monitored closely."
        )
    elif status == "Monitor":
        st.info(
            f"{company} is in Monitor status. Risk is present but currently manageable."
        )
    else:
        st.success(
            f"{company} is Stable. Exposure and vulnerability are currently balanced by resilience."
        )

    st.write(
        f"Exposure: {exposure}, Vulnerability: {vulnerability}, "
        f"Resilience: {resilience}, RII: {rii}."
    )
