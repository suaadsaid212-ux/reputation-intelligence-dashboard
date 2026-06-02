
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import feedparser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Organization Intelligence",
    layout="wide"
)

st.title("Organization Intelligence")

company = st.sidebar.text_input(
    "Enter one company ticker",
    "TSLA"
).strip().upper()

time_range = st.sidebar.selectbox(
    "Analysis Period",
    ["1 Month", "3 Months", "6 Months", "1 Year", "3 Years", "5 Years"]
)

if time_range == "1 Month":
    start_date = "2026-04-01"
elif time_range == "3 Months":
    start_date = "2026-02-01"
elif time_range == "6 Months":
    start_date = "2025-11-01"
elif time_range == "1 Year":
    start_date = "2025-05-01"
elif time_range == "3 Years":
    start_date = "2023-01-01"
else:
    start_date = "2021-01-01"

analyzer = SentimentIntensityAnalyzer()

stock = yf.download(
    company,
    start=start_date,
    progress=False,
    auto_adjust=True
)

if stock.empty:
    st.error("No stock data found. Please check the ticker.")
    st.stop()

stock["Returns"] = stock["Close"].pct_change()
stock["Volatility"] = stock["Returns"].rolling(21).std()

st.subheader(f"{company} Stock Performance")

close_prices = stock["Close"].squeeze()

stock_fig = go.Figure()

stock_fig.add_trace(
    go.Scatter(
        x=close_prices.index,
        y=close_prices.values,
        mode="lines",
        name=company
    )
)

stock_fig.update_layout(
    template="plotly_dark",
    height=550
)

st.plotly_chart(
    stock_fig,
    use_container_width=True
)

st.subheader(f"{company} Volatility Timeline")

volatility_series = stock["Volatility"].fillna(0).squeeze()

vol_fig = go.Figure()

vol_fig.add_trace(
    go.Scatter(
        x=volatility_series.index,
        y=volatility_series.values,
        mode="lines",
        name="Volatility"
    )
)

vol_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    vol_fig,
    use_container_width=True
)

st.subheader(f"{company} News and Sentiment")

rss_url = f"https://news.google.com/rss/search?q={company}"
feed = feedparser.parse(rss_url)

news_rows = []
headlines = []
scores = []

for entry in feed.entries[:20]:
    title = entry.title
    score = analyzer.polarity_scores(title)["compound"]

    if score >= 0.3:
        label = "Positive"
    elif score <= -0.3:
        label = "Negative"
    else:
        label = "Neutral"

    news_rows.append({
        "Headline": title,
        "Sentiment": round(float(score), 3),
        "Label": label
    })

    headlines.append(title)
    scores.append(score)

news_df = pd.DataFrame(news_rows)

st.dataframe(
    news_df,
    use_container_width=True
)

if len(scores) > 0:

    DSS = np.mean(np.abs(scores))
    SV = np.std(scores)
    RR = (0.6 * SV) + (0.4 * DSS)

    col1, col2, col3 = st.columns(3)

    col1.metric("DSS", round(float(DSS), 3))
    col2.metric("Sentiment Volatility", round(float(SV), 3))
    col3.metric("Reputation Risk", round(float(RR), 3))

st.subheader(f"{company} Sentiment Distribution")

if len(news_df) > 0:

    distribution = news_df["Label"].value_counts()

    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=distribution.index,
                values=distribution.values,
                hole=0.45
            )
        ]
    )

    pie_fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )

st.subheader(f"{company} Narrative Word Cloud")

if len(headlines) > 0:

    text = " ".join(headlines)

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="black",
        colormap="Reds"
    ).generate(text)

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    ax.axis("off")

    st.pyplot(fig)

st.subheader(f"{company} DSS Component Heatmap")

if len(scores) > 0:

    Volume = len(headlines) / 20
    Spread = np.std(scores)

    Impact = (
        len([s for s in scores if s < -0.3])
        / len(scores)
    )

    Complexity = (
        np.std([len(h) for h in headlines])
        / 100
    )

    CounterNarrative = (
        len([s for s in scores if s > 0.3])
        / len(scores)
    )

    heatmap_df = pd.DataFrame({
        "Metric": [
            "Volume",
            "Spread",
            "Impact",
            "Complexity",
            "CounterNarrative"
        ],
        "Value": [
            Volume,
            Spread,
            Impact,
            Complexity,
            CounterNarrative
        ]
    })

    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=[heatmap_df["Value"]],
            x=heatmap_df["Metric"],
            y=[company],
            colorscale="Reds"
        )
    )

    heatmap_fig.update_layout(
        template="plotly_dark",
        height=300
    )

    st.plotly_chart(
        heatmap_fig,
        use_container_width=True
    )
