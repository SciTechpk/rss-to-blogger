import feedparser
import requests
import os

# Blogger API Setup
BLOG_ID = os.getenv("BLOG_ID")  # Blogger Blog ID
CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")  # Google API Client ID
CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")  # Google API Client Secret
REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")  # OAuth Refresh Token
RSS_FEED_URL = os.getenv("RSS_FEED_URL")  # RSS Feed URL

# Function to get a new access token
def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    token_info = response.json()
    if "access_token" in token_info:
        return token_info["access_token"]
    else:
        print(f"❌ Error refreshing access token: {token_info}")
        exit(1)

ACCESS_TOKEN = get_access_token()  # Get a fresh access token

def fetch_rss_feed():
    """Fetch latest RSS feed entries."""
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries if feed.entries else []

def format_post(entry):
    """Format post content for Blogger."""
    title = entry.get("title", "No Title")
    link = entry.get("link", "#")
    content = entry.get("summary", "No Content")

    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": f"<p>{content}</p><p>Source: <a href='{link}'>{link}</a></p>",
    }
    return post_data

def post_to_blogger(post_data):
    """Publish a post to Blogger."""
    blogger_api_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(blogger_api_url, json=post_data, headers=headers)

    if response.status_code == 200:
        print(f"✅ Successfully posted: {post_data['title']}")
    else:
        print(f"❌ Failed to post: {response.text}")

def main():
    """Main execution function."""
    print("Fetching RSS feed...")
    posts = fetch_rss_feed()

    if not posts:
        print("No new posts found.")
        return
    
    for entry in posts[:5]:  # Limits to 5 posts per run
        post_data = format_post(entry)
        post_to_blogger(post_data)

if __name__ == "__main__":
    main()
