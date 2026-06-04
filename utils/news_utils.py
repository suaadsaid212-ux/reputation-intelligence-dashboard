import feedparser

def get_news(entity):

    url = (
        f"https://news.google.com/rss/search?q={entity}"
    )

    feed = feedparser.parse(url)

    results = []

    for entry in feed.entries[:20]:

        results.append({

            "title": entry.title,

            "link": entry.link

        })

    return results
