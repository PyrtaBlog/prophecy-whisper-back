import os
import re
from datetime import datetime, timedelta
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_channel_id_from_url(url: str) -> str:
    url = url.strip()
    match = re.search(r"youtube\.com/channel/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    match = re.search(r"youtube\.com/@([a-zA-Z0-9_-]+)", url)
    if match:
        username = match.group(1)
        return resolve_username_to_channel_id(username)
    raise ValueError("Unsupported YouTube channel URL format")

def resolve_username_to_channel_id(username: str) -> str:
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="id", forUsername=username)
    response = request.execute()
    if response.get("items"):
        return response["items"][0]["id"]
    search_request = youtube.search().list(
        part="snippet",
        q=username,
        type="channel",
        maxResults=1
    )
    search_response = search_request.execute()
    if search_response["items"]:
        return search_response["items"][0]["snippet"]["channelId"]
    raise ValueError(f"Channel not found for username: {username}")

def get_channel_name(channel_id: str) -> str:
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="snippet", id=channel_id)
    response = request.execute()
    if response["items"]:
        return response["items"][0]["snippet"]["title"]
    return "Unknown Channel"

def get_latest_videos(channel_id: str, hours: int = 24) -> list:
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    published_after = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        publishedAfter=published_after,
        maxResults=10,
        type="video"
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "publish_date": item["snippet"]["publishedAt"]
        })
    return videos