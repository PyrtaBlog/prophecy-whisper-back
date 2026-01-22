# test_brightdata.py
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

username = os.getenv("BRIGHT_DATA_USERNAME")
password = os.getenv("BRIGHT_DATA_PASSWORD")
proxy_url = f"http://{username}:{password}@brd.superproxy.io:33335"

proxy_config = GenericProxyConfig(
    http_url=proxy_url,
    https_url=proxy_url
)

api = YouTubeTranscriptApi(proxy_config=proxy_config)
print("Testing video IpJ5hMmRnzQ...")
transcript_list = api.list("IpJ5hMmRnzQ")
print("Success! Languages:", [t.language_code for t in transcript_list])