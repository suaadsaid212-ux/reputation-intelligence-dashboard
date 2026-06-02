
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import feedparser
import pydeck as pdk
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Country Exposure",
    layout="wide"
)

st.title("Country Exposure Intelligence")

company_input = st.sidebar.text_input(
    "Enter company tickers",
    "TSLA,MSFT,META,SBER.ME,GAZP.ME,BABA,SONY"
)

companies = [
    c.strip().upper()
    for c in company_input.split(",")
    if c.strip() != ""
]

country_map = {
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
    "SBER.ME": "Russia",
    "GAZP.ME": "Russia",
    "ROSN.ME": "Russia",
    "LKOH.ME": "Russia",
    "YDEX": "Russia",
    "VKCO": "Russia",
    "BABA": "China",
    "TCEHY": "China",
    "SONY": "Japan",
    "TM": "Japan",
    "005930.KS": "South Korea"
}

coordinates = {
    "USA": [37.0902, -95.7129],
    "Russia": [61.5240, 105.3188],
    "China": [35.8617, 104.1954],
    "Japan": [36.2048, 138.2529],
    "South Korea": [35.9078, 127.7669]
}

analyzer = SentimentIntensityAnalyzer()

rows = []

for company in companies:

    country = country_map.get(company, "Unknown")

    if country == "Unknown":
        continue

    rss_url = f"https://news.google.com/rss/search?q={company}"
    feed = feedparser.parse(rss_url)

    scores = []
    negative_count = 0
    total_count = 0

    for entry in feed.entries[:15]:

        score = analyzer.polarity_scores(
            entry.title
        )["compound"]

        scores.append(score)

        total_count += 1

        if score <= -0.3:
            negative_count += 1

    if len(scores) == 0:
        continue

    DSS = np.mean(np.abs(scores))
    SV = np.std(scores)
    RR = (0.6 * SV) + (0.4 * DSS)

    rows.append({
        "Company": company,
        "Country": country,
        "Narrative Volume": total_count,
        "Negative Narratives": negative_count,
        "Average Sentiment": round(float(np.mean(scores)), 3),
        "Sentiment Volatility": round(float(SV), 3),
        "Reputation Risk": round(float(RR), 3)
    })

df = pd.DataFrame(rows)

if df.empty:
    st.error("No country exposure data available.")
    st.stop()

country_df = (
    df.groupby("Country")
    .agg({
        "Company": "count",
        "Narrative Volume": "sum",
        "Negative Narratives": "sum",
        "Average Sentiment": "mean",
        "Sentiment Volatility": "mean",
        "Reputation Risk": "mean"
    })
    .reset_index()
)

country_df = country_df.rename(
    columns={
        "Company": "Organizations Monitored",
        "Reputation Risk": "Average Reputation Risk"
    }
)

st.subheader("Country Exposure Summary")

st.dataframe(
    country_df,
    use_container_width=True
)

st.subheader("Country Risk Ranking")

ranking = country_df.sort_values(
    by="Average Reputation Risk",
    ascending=False
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=ranking["Country"],
        y=ranking["Average Reputation Risk"],
        text=ranking["Average Reputation Risk"],
        textposition="auto"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    title="Average Reputation Risk by Country"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

geo_rows = []

for _, row in country_df.iterrows():

    country = row["Country"]

    if country not in coordinates:
        continue

    lat, lon = coordinates[country]

    geo_rows.append({
        "Country": country,
        "Latitude": lat,
        "Longitude": lon,
        "RiskScore": row["Average Reputation Risk"],
        "Organizations": row["Organizations Monitored"],
        "NarrativeVolume": row["Narrative Volume"]
    })

geo_data = pd.DataFrame(geo_rows)

st.subheader("Geographic Country Risk Map")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=geo_data,
    get_position='[Longitude, Latitude]',
    get_color='[255, 0, 0, 180]',
    get_radius='RiskScore * 2500000',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=30,
    longitude=20,
    zoom=1,
    pitch=30
)

tooltip = {
    "html":
    "<b>Country:</b> {Country}<br/>"
    "<b>Risk Score:</b> {RiskScore}<br/>"
    "<b>Organizations:</b> {Organizations}<br/>"
    "<b>Narrative Volume:</b> {NarrativeVolume}",
    "style": {
        "backgroundColor": "black",
        "color": "white"
    }
}

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style=None
)

st.pydeck_chart(deck)

st.subheader("Organization Exposure by Country")

st.dataframe(
    df.sort_values(
        by=["Country", "Reputation Risk"],
        ascending=[True, False]
    ),
    use_container_width=True
)
