# File: affiliate_to_telegram_bot.py

import requests
import schedule
import time
from telegram import Bot

# Replace with your Amazon PA API credentials
AMAZON_API_KEY = "your_amazon_api_key"
AMAZON_API_SECRET = "your_amazon_api_secret"
AMAZON_ASSOCIATE_TAG = "your_affiliate_tag"

# Replace with your Telegram bot token and group chat ID
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_telegram_group_chat_id"

# Amazon API URL
AMAZON_API_URL = "https://webservices.amazon.in/onca/xml"

# Telegram bot initialization
telegram_bot = Bot(token=TELEGRAM_BOT_TOKEN)


def fetch_top_deals():
    """Fetches the top deals from Amazon using its Product Advertising API."""
    try:
        params = {
            "Service": "AWSECommerceService",
            "Operation": "ItemSearch",
            "SearchIndex": "All",
            "Keywords": "top deals",
            "ResponseGroup": "Images,ItemAttributes,Offers",
            "AWSAccessKeyId": AMAZON_API_KEY,
            "AssociateTag": AMAZON_ASSOCIATE_TAG,
        }
        response = requests.get(AMAZON_API_URL, params=params)
        response.raise_for_status()

        # Parse the response (assuming XML format)
        # Use xml.etree.ElementTree or a library like BeautifulSoup to parse
        # For simplicity, we assume we extract `title`, `link`, and `price`
        deals = []  # Parse and append deal information here
        return deals

    except Exception as e:
        print(f"Error fetching deals: {e}")
        return []


def format_deals(deals):
    """Formats deals into a message for Telegram."""
    if not deals:
        return "No deals found at the moment."

    messages = []
    for deal in deals:
        title = deal.get("title")
        price = deal.get("price")
        link = deal.get("affiliate_link")
        messages.append(f"📌 {title}\n💸 Price: {price}\n🔗 [Buy Now]({link})")
    
    return "\n\n".join(messages)


def post_to_telegram():
    """Fetches top deals and posts them to Telegram."""
    print("Fetching top deals...")
    deals = fetch_top_deals()
    message = format_deals(deals)

    try:
        telegram_bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown"
        )
        print("Posted to Telegram successfully!")
    except Exception as e:
        print(f"Error posting to Telegram: {e}")


# Schedule the script to run hourly
schedule.every().hour.at(":00").do(post_to_telegram)

if __name__ == "__main__":
    print("Affiliate Marketing Bot started...")
    while True:
        schedule.run_pending()
        time.sleep(1)
