import feedparser
import requests
import os

# Blogger API Setup
BLOG_ID = os.getenv("BLOG_ID")  # Your Blogger Blog ID (stored as a secret in GitHub)
API_KEY = os.getenv("API_KEY")  # Your Blogger API Key (stored as a secret in GitHub)
RSS_FEED_URL = os.getenv("RSS_FEED_URL")  # RSS Feed URL (stored as a secret in GitHub)

# Blogger API Endpoint
BLOGGER_API_URL = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"

def fetch_rss_feed():
    """Fetch the latest posts from the RSS feed."""
    try:
        feed = feedparser.parse(RSS_FEED_URL)
        return feed.entries
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []

def format_post(entry):
    """Format the post content for Blogger."""
    title = entry.get("title", "No Title")
    link = entry.get("link", "")
    content = entry.get("summary", "No Content")

    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": f"<p>{content}</p><p>Source: <a href='{link}'>{link}</a></p>",
    }
    return post_data

def post_to_blogger(post_data):
    """Publish a post to Blogger."""
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(BLOGGER_API_URL, json=post_data, headers=headers)

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
