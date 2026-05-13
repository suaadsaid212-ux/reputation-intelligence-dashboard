
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import feedparser
import pydeck as pdk
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Reputation Intelligence System",
    layout="wide"
)

# =====================================
# LANGUAGE SELECTOR
# =====================================

language = st.sidebar.selectbox(

    "Language / Язык",

    ["EN", "RU"]
)

# =====================================
# TRANSLATIONS
# =====================================

if language == "RU":

    dashboard_title = (
        "Система репутационного интеллекта"
    )

    stock_title = (
        "Сравнительный анализ акций"
    )

    metrics_title = (
        "Метрики репутационного риска"
    )

    input_title = (
        "Введите тикеры компаний"
    )

else:

    dashboard_title = (
        "Reputation Intelligence System"
    )

    stock_title = (
        "Comparative Stock Analysis"
    )

    metrics_title = (
        "Reputation Intelligence Metrics"
    )

    input_title = (
        "Enter company tickers"
    )

# =====================================
# TITLE
# =====================================

st.title(dashboard_title)

# =====================================
# =====================================
# TIME RANGE SELECTOR
# =====================================

if language == "RU":

    time_title = "Период анализа"

    ticker_title = "Введите тикеры компаний"

else:

    time_title = "Analysis Period"

    ticker_title = "Enter company tickers"

time_range = st.sidebar.selectbox(

    time_title,

    [

        "1 Month",
        "3 Months",
        "6 Months",
        "1 Year",
        "3 Years",
        "5 Years"
    ]
)

# =====================================
# PERIOD LOGIC
# =====================================

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

# =====================================
# COMPANY INPUT
# =====================================

company_input = st.sidebar.text_input(

    ticker_title,

    "TSLA,MSFT,META"
)

companies = [

    c.strip()

    for c in company_input.split(",")
]
# =====================================
# DOWNLOAD DATA
# =====================================

multi_data = {}

for company in companies:

    stock = yf.download(

        company,

        start=start_date,

        progress=False,

        auto_adjust=True
    )

    stock["Returns"] = (

        stock["Close"]

        .pct_change()
    )

    stock["Volatility"] = (

        stock["Returns"]

        .rolling(21)

        .std()
    )

    multi_data[company] = stock

# =====================================
# STOCK CHART
# =====================================

st.subheader(stock_title)

fig = go.Figure()

for company in companies:

    close_prices = (

        multi_data[company]["Close"]

        .squeeze()
    )

    fig.add_trace(

        go.Scatter(

            x=close_prices.index,

            y=close_prices.values,

            mode="lines",

            name=company
        )
    )

fig.update_layout(

    template="plotly_dark",

    height=600
)

st.plotly_chart(

    fig,

    use_container_width=True
)

# =====================================
# NEWS ANALYSIS
# =====================================

analyzer = SentimentIntensityAnalyzer()

results = []

for company in companies:

    rss_url = (

        f"https://news.google.com/rss/search?q={company}"
    )

    feed = feedparser.parse(rss_url)

    scores = []

    for entry in feed.entries[:10]:

        sentiment = analyzer.polarity_scores(

            entry.title
        )

        scores.append(

            sentiment["compound"]
        )

    if len(scores) == 0:

        continue

    DSS = np.mean(np.abs(scores))

    SV = np.std(scores)

    RR = (

        0.6 * SV

    ) + (

        0.4 * DSS
    )

    results.append({

        "Company": company,

        "DSS":
        round(float(DSS), 3),

        "Sentiment Volatility":
        round(float(SV), 3),

        "Reputation Risk":
        round(float(RR), 3)
    })

real_dss_df = pd.DataFrame(results)

# =====================================
# METRICS TABLE
# =====================================

st.subheader(metrics_title)

st.dataframe(
    real_dss_df,
    use_container_width=True
)
# =====================================
# HIGH RISK NARRATIVES
# =====================================

keyword_results = []

for company in companies:

    rss_url = (
        f"https://news.google.com/rss/search?q={company}"
    )

    feed = feedparser.parse(rss_url)

    for entry in feed.entries[:10]:

        title = entry.title

        sentiment = analyzer.polarity_scores(title)

        score = sentiment["compound"]

        if score <= -0.2:

            keyword_results.append({

                "Company": company,

                "Headline": title,

                "Sentiment": round(score, 3),

                "Risk Level": "Negative Narrative"
            })

keyword_df = pd.DataFrame(keyword_results)

st.subheader("High Risk Narratives")

st.dataframe(
    keyword_df,
    use_container_width=True
)

# =====================================
# WORD CLOUD ANALYSIS
# =====================================

st.subheader("Narrative Word Cloud")

for company in companies:

    rss_url = (
        f"https://news.google.com/rss/search?q={company}"
    )

    feed = feedparser.parse(rss_url)

    headlines = []

    for entry in feed.entries[:20]:

        headlines.append(
            entry.title
        )

    if len(headlines) == 0:

        continue

    text = " ".join(headlines)

    wordcloud = WordCloud(

        width=1200,

        height=600,

        background_color="black",

        colormap="Reds"

    ).generate(text)

    fig, ax = plt.subplots(

        figsize=(14, 7)
    )

    ax.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    ax.axis("off")

    ax.set_title(

        f"{company} Narrative Keywords",

        fontsize=20
    )

    st.pyplot(fig)

# =====================================
# COMPANY SENTIMENT DISTRIBUTION
# =====================================

st.subheader("Company Sentiment Distribution")

for company in companies:

    rss_url = (
        f"https://news.google.com/rss/search?q={company}"
    )

    feed = feedparser.parse(rss_url)

    labels = []

    for entry in feed.entries[:15]:

        score = analyzer.polarity_scores(
            entry.title
        )["compound"]

        if score >= 0.3:

            labels.append("Positive")

        elif score <= -0.3:

            labels.append("Negative")

        else:

            labels.append("Neutral")

    if len(labels) == 0:

        continue

    distribution = (
        pd.Series(labels)
        .value_counts()
    )

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

        title=f"{company} Narrative Sentiment",

        template="plotly_dark",

        height=500
    )

    st.plotly_chart(

        pie_fig,

        use_container_width=True
    )

# =====================================
# DSS HEATMAPS
# =====================================

st.subheader("DSS Component Heatmaps")

for company in companies:

    rss_url = (
        f"https://news.google.com/rss/search?q={company}"
    )

    feed = feedparser.parse(rss_url)

    headlines = []

    scores = []

    for entry in feed.entries[:15]:

        headlines.append(entry.title)

        sentiment = analyzer.polarity_scores(
            entry.title
        )

        scores.append(
            sentiment["compound"]
        )

    if len(scores) == 0:

        continue

    # DSS VARIABLES

    Volume = len(headlines) / 15

    Spread = np.std(scores)

    negative_ratio = (
        len([s for s in scores if s < -0.3])
        / len(scores)
    )

    Impact = negative_ratio

    Complexity = (
        np.std([len(h) for h in headlines])
        / 100
    )

    positive_ratio = (
        len([s for s in scores if s > 0.3])
        / len(scores)
    )

    CounterNarrative = positive_ratio

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

        title=f"{company} DSS Heatmap",

        template="plotly_dark",

        height=300
    )

    st.plotly_chart(

        heatmap_fig,

        use_container_width=True
    )

# =====================================
# COMPANY → COUNTRY MAP
# =====================================

country_map = {

    # USA
    "TSLA": "USA",
    "MSFT": "USA",
    "META": "USA",
    "AAPL": "USA",
    "GOOGL": "USA",
    "AMZN": "USA",
    "NVDA": "USA",
    "NFLX": "USA",
    "IBM": "USA",
    "INTC": "USA",

    # Russia
    "SBER.ME": "Russia",
    "GAZP.ME": "Russia",
    "ROSN.ME": "Russia",
    "LKOH.ME": "Russia",
    "YDEX": "Russia",
    "VKCO": "Russia",

    # China
    "BABA": "China",
    "TCEHY": "China",

    # Japan
    "SONY": "Japan",
    "TM": "Japan",

    # South Korea
    "005930.KS": "South Korea"
}

# =====================================
# COUNTRY COORDINATES
# =====================================

coordinates = {

    "USA": [37.0902, -95.7129],

    "Russia": [61.5240, 105.3188],

    "China": [35.8617, 104.1954],

    "Japan": [36.2048, 138.2529],

    "South Korea": [35.9078, 127.7669]
}

# =====================================
# BUILD GEO DATA
# =====================================

geo_rows = []

for i in range(len(real_dss_df)):

    company = real_dss_df.iloc[i]["Company"]

    risk = real_dss_df.iloc[i][
        "Reputation Risk"
    ]

    country = country_map.get(
        company,
        "USA"
    )

    lat, lon = coordinates[country]

    geo_rows.append({

        "Company": company,

        "Country": country,

        "Latitude": lat,

        "Longitude": lon,

        "RiskScore": risk
    })

geo_data = pd.DataFrame(geo_rows)

# =====================================
# MAP TITLE
# =====================================

if language == "RU":

    map_title = (
        "Глобальная карта репутационных рисков"
    )

else:

    map_title = (
        "Global Reputation Risk Map"
    )

st.subheader(map_title)

# =====================================
# MAP LAYER
# =====================================

layer = pdk.Layer(

    "ScatterplotLayer",

    data=geo_data,

    get_position='[Longitude, Latitude]',

    get_color='[255, 0, 0, 180]',

    get_radius='RiskScore * 1200000',

    pickable=True
)

# =====================================
# VIEW STATE
# =====================================

view_state = pdk.ViewState(

    latitude=30,

    longitude=20,

    zoom=1,

    pitch=30
)

# =====================================
# TOOLTIP
# =====================================

tooltip = {

    "html":
    "<b>Company:</b> {Company}<br/>"
    "<b>Country:</b> {Country}<br/>"
    "<b>Risk:</b> {RiskScore}",

    "style": {

        "backgroundColor": "black",

        "color": "white"
    }
}

# =====================================
# MAP OBJECT
# =====================================

r = pdk.Deck(

    layers=[layer],

    initial_view_state=view_state,

    tooltip=tooltip,

    map_style=None
)

# =====================================
# DISPLAY MAP
# =====================================

st.pydeck_chart(r)
# =====================================
# ALERT ENGINE
# =====================================

st.subheader("Risk Alert Engine")

for i in range(len(real_dss_df)):

    company = real_dss_df.iloc[i]["Company"]

    dss = real_dss_df.iloc[i]["DSS"]

    sv = real_dss_df.iloc[i][
        "Sentiment Volatility"
    ]

    rr = real_dss_df.iloc[i][
        "Reputation Risk"
    ]

    if rr >= 1.5:

        st.error(
            f"{company}: HIGH REPUTATION RISK DETECTED"
        )

    elif rr >= 0.7:

        st.warning(
            f"{company}: MODERATE REPUTATION RISK"
        )

    else:

        st.success(
            f"{company}: LOW REPUTATION RISK"
        )

# =====================================
# TOP NEGATIVE NARRATIVES
# =====================================

st.subheader("Top Negative Narratives")

if keyword_df.empty:

    st.info(
        "No high-risk negative narratives detected."
    )

else:

    negative_df = keyword_df.sort_values(

        by="Sentiment"

    ).head(10)

    st.dataframe(

        negative_df,

        use_container_width=True
    )

# =====================================
# COMPANY RANKING
# =====================================

st.subheader("Company Risk Ranking")

ranking_df = real_dss_df.sort_values(

    by="Reputation Risk",

    ascending=False
)

ranking_df["Rank"] = range(

    1,

    len(ranking_df) + 1
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================
# KPI CARDS
# =====================================

st.subheader("Executive KPI Overview")

avg_dss = round(
    real_dss_df["DSS"].mean(),
    3
)

avg_rr = round(
    real_dss_df["Reputation Risk"].mean(),
    3
)

avg_sv = round(
    real_dss_df[
        "Sentiment Volatility"
    ].mean(),
    3
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average DSS",
    avg_dss
)

col2.metric(
    "Average Reputation Risk",
    avg_rr
)

col3.metric(
    "Average Sentiment Volatility",
    avg_sv
)

# =====================================
# TIME-BASED RISK EVOLUTION
# =====================================

st.subheader("Risk Evolution Timeline")

timeline_fig = go.Figure()

for company in companies:

    stock_df = multi_data[company]

    risk_series = (
        stock_df["Volatility"]
        .fillna(0)
        .squeeze()
    )

    timeline_fig.add_trace(

        go.Scatter(

            x=risk_series.index,

            y=risk_series.values,

            mode="lines",

            name=company
        )
    )

timeline_fig.update_layout(

    title="Risk Volatility Over Time",

    template="plotly_dark",

    height=600
)

st.plotly_chart(
    timeline_fig,
    use_container_width=True
)

# =====================================
# EXECUTIVE AI-STYLE INSIGHTS
# =====================================

st.subheader("Executive Intelligence Insights")

for i in range(len(real_dss_df)):

    company = real_dss_df.iloc[i]["Company"]

    dss = real_dss_df.iloc[i]["DSS"]

    sv = real_dss_df.iloc[i][
        "Sentiment Volatility"
    ]

    rr = real_dss_df.iloc[i][
        "Reputation Risk"
    ]

    if rr >= 1.5:

        insight = (
            f"{company} demonstrates severe "
            f"reputational instability driven "
            f"by elevated sentiment volatility "
            f"and disinformation exposure."
        )

    elif rr >= 0.7:

        insight = (
            f"{company} demonstrates moderate "
            f"reputational pressure with "
            f"increasing narrative volatility."
        )

    else:

        insight = (
            f"{company} currently maintains "
            f"relatively stable reputation "
            f"conditions with limited negative "
            f"narrative escalation."
        )

    st.info(insight)

# =====================================
# SECTOR ANALYSIS
# =====================================

st.subheader("Sector Intelligence")

sector_map = {

    "TSLA": "Automotive",

    "MSFT": "Technology",

    "META": "Social Media",

    "AAPL": "Technology",

    "GOOGL": "Technology",

    "AMZN": "E-Commerce",

    "NVDA": "Semiconductors",

    "SBER.ME": "Banking",

    "GAZP.ME": "Energy",

    "BABA": "E-Commerce",

    "SONY": "Electronics"
}

sector_rows = []

for i in range(len(real_dss_df)):

    company = real_dss_df.iloc[i]["Company"]

    rr = real_dss_df.iloc[i][
        "Reputation Risk"
    ]

    sector = sector_map.get(
        company,
        "Other"
    )

    sector_rows.append({

        "Company": company,

        "Sector": sector,

        "Reputation Risk": rr
    })

sector_df = pd.DataFrame(sector_rows)

sector_fig = go.Figure()

for sector in sector_df["Sector"].unique():

    sector_subset = sector_df[
        sector_df["Sector"] == sector
    ]

    sector_fig.add_trace(

        go.Bar(

            x=sector_subset["Company"],

            y=sector_subset[
                "Reputation Risk"
            ],

            name=sector
        )
    )

sector_fig.update_layout(

    title="Sector Reputation Risk Comparison",

    template="plotly_dark",

    height=600
)

st.plotly_chart(
    sector_fig,
    use_container_width=True
)
