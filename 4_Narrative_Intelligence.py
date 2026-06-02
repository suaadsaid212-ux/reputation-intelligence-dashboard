
import streamlit as st
import pandas as pd
import feedparser
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Narrative Intelligence",
    layout="wide"
)

st.title("Narrative Intelligence")

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

        title = entry.title
        score = analyzer.polarity_scores(title)["compound"]

        if score >= 0.3:
            label = "Positive"
        elif score <= -0.3:
            label = "Negative"
        else:
            label = "Neutral"

        if score <= -0.5:
            risk_label = "High Risk Narrative"
        elif score <= -0.2:
            risk_label = "Moderate Risk Narrative"
        else:
            risk_label = "Low Risk Narrative"

        rows.append({
            "Company": company,
            "Headline": title,
            "Sentiment": round(float(score), 3),
            "Sentiment Label": label,
            "Narrative Risk": risk_label
        })

narrative_df = pd.DataFrame(rows)

if narrative_df.empty:
    st.error("No narrative data available.")
    st.stop()

st.subheader("Narrative Feed")

st.dataframe(
    narrative_df,
    use_container_width=True
)

st.subheader("High-Risk Narratives")

high_risk_df = narrative_df[
    narrative_df["Narrative Risk"] != "Low Risk Narrative"
]

if high_risk_df.empty:
    st.info("No high-risk narratives detected.")
else:
    st.dataframe(
        high_risk_df.sort_values(
            by="Sentiment"
        ),
        use_container_width=True
    )

st.subheader("Narrative Sentiment Distribution")

sentiment_counts = (
    narrative_df["Sentiment Label"]
    .value_counts()
)

pie_fig = go.Figure(
    data=[
        go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
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

st.subheader("Narrative Risk Distribution")

risk_counts = (
    narrative_df["Narrative Risk"]
    .value_counts()
)

risk_fig = go.Figure()

risk_fig.add_trace(
    go.Bar(
        x=risk_counts.index,
        y=risk_counts.values,
        text=risk_counts.values,
        textposition="auto"
    )
)

risk_fig.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(
    risk_fig,
    use_container_width=True
)

st.subheader("Company Narrative Word Clouds")

for company in companies:

    company_df = narrative_df[
        narrative_df["Company"] == company
    ]

    text = " ".join(
        company_df["Headline"].tolist()
    )

    if text.strip() == "":
        continue

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

st.subheader("Most Negative Narratives by Company")

for company in companies:

    company_df = narrative_df[
        narrative_df["Company"] == company
    ]

    company_negative = company_df.sort_values(
        by="Sentiment"
    ).head(5)

    st.write(f"### {company}")

    st.dataframe(
        company_negative,
        use_container_width=True
    )
