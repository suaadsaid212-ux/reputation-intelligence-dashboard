
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Executive Overview",
    layout="wide"
)

st.title("Executive Overview")

language = st.sidebar.selectbox(
    "Language / Язык",
    ["EN", "RU"]
)

if language == "RU":
    input_title = "Введите тикеры компаний"
    period_title = "Период анализа"
    page_title = "Исполнительная панель"
else:
    input_title = "Enter company tickers"
    period_title = "Analysis Period"
    page_title = "Executive Overview"

st.header(page_title)

time_range = st.sidebar.selectbox(
    period_title,
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

company_input = st.sidebar.text_input(
    input_title,
    "TSLA,MSFT,META"
)

companies = [
    c.strip().upper()
    for c in company_input.split(",")
    if c.strip() != ""
]

analyzer = SentimentIntensityAnalyzer()

results = []
keyword_results = []

for company in companies:

    stock = yf.download(
        company,
        start=start_date,
        progress=False,
        auto_adjust=True
    )

    if stock.empty:
        st.warning(f"No stock data found for {company}")
        continue

    stock["Returns"] = stock["Close"].pct_change()
    stock["Volatility"] = stock["Returns"].rolling(21).std()

    latest_volatility = stock["Volatility"].dropna()

    if len(latest_volatility) == 0:
        market_volatility = 0
    else:
        market_volatility = float(latest_volatility.iloc[-1])

    rss_url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(rss_url)

    scores = []

    for entry in feed.entries[:15]:
        title = entry.title
        score = analyzer.polarity_scores(title)["compound"]
        scores.append(score)

        if score <= -0.2:
            keyword_results.append({
                "Company": company,
                "Headline": title,
                "Sentiment": round(float(score), 3),
                "Risk Level": "Negative Narrative"
            })

    if len(scores) == 0:
        continue

    DSS = np.mean(np.abs(scores))
    SV = np.std(scores)
    RR = (0.6 * SV) + (0.4 * DSS)

    if RR >= 1.5:
        risk_level = "High"
    elif RR >= 0.7:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    results.append({
        "Company": company,
        "DSS": round(float(DSS), 3),
        "Sentiment Volatility": round(float(SV), 3),
        "Market Volatility": round(float(market_volatility), 4),
        "Reputation Risk": round(float(RR), 3),
        "Risk Level": risk_level
    })

risk_df = pd.DataFrame(results)
keyword_df = pd.DataFrame(keyword_results)

if risk_df.empty:
    st.error("No data available. Try different tickers.")
    st.stop()

avg_dss = round(risk_df["DSS"].mean(), 3)
avg_rr = round(risk_df["Reputation Risk"].mean(), 3)
avg_sv = round(risk_df["Sentiment Volatility"].mean(), 3)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average DSS", avg_dss)
col2.metric("Average Reputation Risk", avg_rr)
col3.metric("Average Sentiment Volatility", avg_sv)
col4.metric("Companies Monitored", len(risk_df))

st.subheader("Company Risk Ranking")

ranking_df = risk_df.sort_values(
    by="Reputation Risk",
    ascending=False
)

ranking_df["Rank"] = range(1, len(ranking_df) + 1)

st.dataframe(
    ranking_df,
    use_container_width=True
)

st.subheader("Risk Alert Engine")

for _, row in ranking_df.iterrows():

    company = row["Company"]
    rr = row["Reputation Risk"]

    if rr >= 1.5:
        st.error(f"{company}: HIGH REPUTATION RISK DETECTED")
    elif rr >= 0.7:
        st.warning(f"{company}: MODERATE REPUTATION RISK")
    else:
        st.success(f"{company}: LOW REPUTATION RISK")

st.subheader("Top Negative Narratives")

if keyword_df.empty:
    st.info("No high-risk negative narratives detected.")
else:
    negative_df = keyword_df.sort_values(
        by="Sentiment"
    ).head(10)

    st.dataframe(
        negative_df,
        use_container_width=True
    )

st.subheader("Executive Intelligence Insights")

for _, row in ranking_df.iterrows():

    company = row["Company"]
    rr = row["Reputation Risk"]

    if rr >= 1.5:
        insight = (
            f"{company} demonstrates severe reputational instability "
            f"driven by elevated sentiment volatility and negative narrative exposure."
        )
    elif rr >= 0.7:
        insight = (
            f"{company} demonstrates moderate reputational pressure "
            f"with increasing narrative volatility."
        )
    else:
        insight = (
            f"{company} currently maintains relatively stable reputation conditions "
            f"with limited negative narrative escalation."
        )

    st.info(insight)
