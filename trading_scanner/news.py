from __future__ import annotations

from datetime import datetime, timedelta, timezone
import time
from typing import List, Dict

import feedparser

POSITIVE_WORDS = {
    "beats", "beat", "upgrade", "upgrades", "bullish", "surge", "surges",
    "soars", "soar", "jumps", "jump", "breakout", "strong", "growth",
    "guidance raised", "raised guidance", "record", "momentum", "buyback",
    "partnership", "expands", "expansion", "outperform", "rebound", "rebounds",
    "higher", "gain", "gains", "wins", "win"
}

NEGATIVE_WORDS = {
    "miss", "misses", "downgrade", "downgrades", "bearish", "falls", "drop",
    "drops", "slides", "slide", "lawsuit", "investigation", "cuts guidance",
    "guidance cut", "weak", "decline", "declines", "breakdown", "risk",
    "recall", "plunge", "plunges", "underperform", "warning", "selloff",
    "lower", "loss", "losses"
}


def fetch_yahoo_news(ticker: str, news_hours: int = 48) -> List[Dict[str, str]]:
    url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    feed = feedparser.parse(url)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=news_hours)
    items: List[Dict[str, str]] = []

    for entry in getattr(feed, 'entries', []):
        published_parsed = getattr(entry, 'published_parsed', None)
        if published_parsed is None:
            continue
        published_dt = datetime.fromtimestamp(time.mktime(published_parsed), tz=timezone.utc)
        if published_dt < cutoff:
            continue
        items.append({
            'title': entry.title,
            'link': getattr(entry, 'link', ''),
            'published': published_dt.isoformat(),
        })

    return items


def headline_sentiment_score(headlines: List[Dict[str, str]]) -> int:
    score = 0
    for item in headlines:
        title = item['title'].lower()
        for word in POSITIVE_WORDS:
            if word in title:
                score += 1
        for word in NEGATIVE_WORDS:
            if word in title:
                score -= 1
    return score


def summarize_top_headline(headlines: List[Dict[str, str]]) -> str:
    if not headlines:
        return ''
    headlines = sorted(headlines, key=lambda x: x['published'], reverse=True)
    return headlines[0]['title']
