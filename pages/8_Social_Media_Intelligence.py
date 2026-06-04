import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils.entity_selector import get_entity, get_entity_query

st.set_page_config(
    page_title="Social Media Intelligence",
    page_icon="📱",
    layout="wide",
)

entity = get_entity()

organization = entity["Entity_Name"]
display_name = entity["Short_Name"]
youtube_query = get_entity_query(entity, "YouTube_Query")

st.title("📱 Social Media Intelligence")

st.markdown(f"""
### Monitoring Social Reputation Signals

**Selected Entity:** {display_name}

**YouTube Query:** {youtube_query}

Sources:

- YouTube real data, if API key is available
- Reddit demo data, until Reddit API is connected
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Type", entity["Entity_Type"])
c2.metric("Country", entity["Country"])
c3.metric("Sector", entity["Sector"])
c4.metric("Priority", entity["Priority"])

st.divider()

analyzer = SentimentIntensityAnalyzer()


def get_secret_value(name):
    try:
        return st.secrets[name]
    except Exception:
        return ""


@st.cache_data(ttl=3600)
def get_youtube_data(query, api_key):
    if not api_key:
        return pd.DataFrame()

    search_url = "https://www.googleapis.com/youtube/v3/search"

    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 25,
        "order": "relevance",
        "key": api_key,
    }

    search_response = requests.get(
        search_url,
        params=search_params,
        timeout=20,
    )

    search_response.raise_for_status()

    search_data = search_response.json()
    video_ids = []

    rows = []

    for item in search_data.get("items", []):
        video_id = item.get("id", {}).get("videoId")

        if not video_id:
            continue

        video_ids.append(video_id)

        snippet = item.get("snippet", {})

        rows.append({
            "Video_ID": video_id,
            "Title": snippet.get("title", ""),
            "Channel": snippet.get("channelTitle", ""),
            "Published_At": snippet.get("publishedAt", ""),
        })

    if not video_ids:
        return pd.DataFrame()

    stats_url = "https://www.googleapis.com/youtube/v3/videos"

    stats_params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": api_key,
    }

    stats_response = requests.get(
        stats_url,
        params=stats_params,
        timeout=20,
    )

    stats_response.raise_for_status()

    stats_data = stats_response.json()

    stats_by_id = {}

    for item in stats_data.get("items", []):
        video_id = item.get("id")
        statistics = item.get("statistics", {})

        stats_by_id[video_id] = {
            "Views": int(statistics.get("viewCount", 0)),
            "Likes": int(statistics.get("likeCount", 0)),
            "Comments": int(statistics.get("commentCount", 0)),
        }

    for row in rows:
        stats = stats_by_id.get(
            row["Video_ID"],
            {
                "Views": 0,
                "Likes": 0,
                "Comments": 0,
            },
        )

        row.update(stats)

        sentiment = analyzer.polarity_scores(
            row["Title"]
        )["compound"]

        row["Sentiment"] = sentiment

    return pd.DataFrame(rows)


youtube_api_key = get_secret_value("YOUTUBE_API_KEY")

try:
    youtube_df = get_youtube_data(
        youtube_query,
        youtube_api_key,
    )
except Exception as error:
    st.warning("YouTube data could not be loaded.")
    st.code(str(error))
    youtube_df = pd.DataFrame()

using_real_youtube = not youtube_df.empty

if using_real_youtube:
    youtube_mentions = len(youtube_df)
    youtube_engagement = int(
        youtube_df["Views"].sum()
        + youtube_df["Likes"].sum()
        + youtube_df["Comments"].sum()
    )
    youtube_sentiment = float(youtube_df["Sentiment"].mean())

else:
    st.info(
        "Using demo YouTube values. Add YOUTUBE_API_KEY to Streamlit secrets "
        "to use real YouTube data."
    )

    np.random.seed(42)

    youtube_mentions = np.random.randint(500, 3000)
    youtube_engagement = np.random.randint(10000, 100000)
    youtube_sentiment = np.random.uniform(-1, 1)

np.random.seed(43)

reddit_mentions = np.random.randint(100, 1500)
reddit_sentiment = np.random.uniform(-1, 1)
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

k1, k2, k3, k4 = st.columns(4)

k1.metric("SSI", ssi)
k2.metric("SVI", svi)
k3.metric("NPI", npi)
k4.metric("SRS", srs)

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
