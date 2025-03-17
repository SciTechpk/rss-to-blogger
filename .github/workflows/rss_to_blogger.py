import os
import requests
import feedparser
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Load environment variables
CLIENT_ID = os.getenv('BLOGGER_CLIENT_ID')
CLIENT_SECRET = os.getenv('BLOGGER_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('BLOGGER_REFRESH_TOKEN')
BLOG_ID = os.getenv('BLOG_ID')
RSS_FEED_URL = os.getenv('RSS_FEED_URL')

# Function to get new access token
def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

# Function to post to Blogger
def post_to_blogger(title, content):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"kind": "blogger#post", "title": title, "content": content}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Fetch RSS feed and post latest article
feed = feedparser.parse(RSS_FEED_URL)
latest_entry = feed.entries[0]
title = latest_entry.title
content = latest_entry.summary

# Post to Blogger
post_response = post_to_blogger(title, content)
print(f"Posted: {post_response.get('url', 'Error')}")
