import requests
import json
from datetime import datetime

# Webhook URLs for each category
WEBHOOKS = {
    "geopolitics": "https://discord.com/api/webhooks/1309822984797556807/o_U72xbAHtftWgWzgARCvFVoSDdzx6Bn1Ck0U0Uk79wgOVQTeBuHPxZfPMoZvvn-ucS5",  # Replace with your actual Discord webhook URL
    "cyber_threats": "https://discord.com/api/webhooks/1309822988509646878/Lk0GWoccA6TdEqYCtTZO0ZFFP13lJhPuakCUdys8WB_vud9RbjguEAws5KGh34lG97L5",  # Replace with your actual Discord webhook URL
    # "osint_tools": "YOUR_WEBHOOK_URL_3",  # Replace with your actual Discord webhook URL
    "nepal": "https://discord.com/api/webhooks/1309823188527747083/4xhL7zA5pcD5ommAiAYwbErIQ7d_4tWCmmBP6lES5HQdCrzUvOGm0XXfO7OEdylHDP8-"
}

# News API Key (sign up at https://newsapi.org/ to get an API key)
NEWS_API_KEY = "9823c4a7f17948e4b16ef34824ff287f"  # Replace with your actual API key

# News categories and their keywords
CATEGORIES = {
    "nepal":["kathmandu","delhi"],
    "geopolitics": ["Nepal", "India", "China", "geopolitics", "diplomacy"],
    "cyber_threats": ["cybersecurity", "hacking", "ransomware", "malware", "vulnerabilities", "phishing","bugs","cve","software"],
    # "osint_tools": ["OSINT", "intelligence", "geospatial", "investigation", "data analysis"],
}

# Function to fetch news for a specific category
def fetch_news(keywords):
    url = f"https://newsapi.org/v2/everything"
    params = {
        "q": " OR ".join(keywords),
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,  # Fetch the latest 5 articles
        "source": "google-news-in,bbc-news,cnn,the-hindu,the-hacker-news,ary-news,ndtv,times-of-india,dawn,geo-news,hindustan-times,economictimes,al-jazeera-english,deccan-herald,express-tribune,firstpost,news18"    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        news_items = []
        for article in articles:
            title = article["title"]
            url = article["url"]
            source = article["source"]["name"]
            news_items.append(f"**{title}**\nSource: {source}\n[Read more]({url})\n")
        return news_items
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

# Function to send news to a Discord webhook
def send_news(webhook_url, category, news_items):
    if not news_items:
        content = f"**No new updates for {category.title()} at this time.**"
    else:
        content = f"**{category.title()} Updates:**\n" + "\n".join(news_items)
    payload = {"content": content}
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print(f"News sent to {category} webhook successfully!")
    else:
        print(f"Failed to send news to {category} webhook: {response.status_code}")

# Main function
def main():
    print(f"Running news bot at {datetime.now()}...\n")
    for category, keywords in CATEGORIES.items():
        print(f"Fetching news for {category}...")
        news_items = fetch_news(keywords)
        webhook_url = WEBHOOKS.get(category)
        if webhook_url:
            print(f"Sending news to {category} webhook...")
            send_news(webhook_url, category, news_items)
        else:
            print(f"No webhook URL set for {category}.")
    print("Done.")

if __name__ == "__main__":
    main()
