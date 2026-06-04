import random
import requests
import pandas as pd

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_social_score(query, youtube_api_key=""):
    query = str(query).strip()

    if not query or query.lower() == "nan":
        return {
            "mentions": 0,
            "sentiment": 0,
            "engagement": 0,
            "source": "empty_query",
        }

    if youtube_api_key:
        youtube_result = get_youtube_score(
            query,
            youtube_api_key,
        )

        if youtube_result["source"] == "youtube_api":
            return youtube_result

    return get_demo_social_score(query)


def get_demo_social_score(query):
    random.seed(query)

    return {
        "mentions": random.randint(100, 10000),
        "sentiment": round(random.uniform(-1, 1), 2),
        "engagement": random.randint(1000, 100000),
        "source": "demo_fallback",
    }


def get_youtube_score(query, youtube_api_key):
    analyzer = SentimentIntensityAnalyzer()

    try:
        search_response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 25,
                "order": "relevance",
                "key": youtube_api_key,
            },
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

            title = item.get("snippet", {}).get("title", "")

            rows.append({
                "Video_ID": video_id,
                "Title": title,
                "Sentiment": analyzer.polarity_scores(title)["compound"],
            })

        if not video_ids:
            return get_demo_social_score(query)

        stats_response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={
                "part": "statistics",
                "id": ",".join(video_ids),
                "key": youtube_api_key,
            },
            timeout=20,
        )

        stats_response.raise_for_status()

        stats_data = stats_response.json()
        stats_by_id = {}

        for item in stats_data.get("items", []):
            stats = item.get("statistics", {})

            stats_by_id[item.get("id")] = {
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
            }

        for row in rows:
            stats = stats_by_id.get(
                row["Video_ID"],
                {
                    "views": 0,
                    "likes": 0,
                    "comments": 0,
                },
            )

            row.update(stats)

        df = pd.DataFrame(rows)

        engagement = int(
            df["views"].sum()
            + df["likes"].sum()
            + df["comments"].sum()
        )

        return {
            "mentions": len(df),
            "sentiment": round(float(df["Sentiment"].mean()), 2),
            "engagement": engagement,
            "source": "youtube_api",
        }

    except Exception:
        return get_demo_social_score(query)
