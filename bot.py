import os
import random
import requests
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_random_15min_abs_workout():
    """
    Searches YouTube for 15-minute abs workout videos using yt-dlp,
    filters for videos between 14 and 16 minutes, and returns a random video's URL.
    """
    search_query = "ytsearch20:15 minute abs workout"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # Only extract metadata
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_result = ydl.extract_info(search_query, download=False)
        except Exception as e:
            print("Error during YouTube search:", e)
            return None

    filtered_entries = []
    for entry in search_result.get('entries', []):
        duration = entry.get('duration')
        # Filter for videos approximately 15 minutes long (14-16 minutes)
        if duration and 14 * 60 <= duration <= 16 * 60:
            filtered_entries.append(entry)
    
    if not filtered_entries:
        return None
    
    video = random.choice(filtered_entries)
    return f"https://www.youtube.com/watch?v={video.get('id')}"

def send_telegram_message(video_url):
    """
    Sends a message containing the video URL to a Telegram group using the Telegram Bot API.
    Expects TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to be set in the environment.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables.")
        return
    
    message = f"Good morning! Here’s your 15-minute abs workout for today: {video_url}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.get(url, params=payload)
        print("Message sent:", response.text)
    except Exception as e:
        print("Error sending Telegram message:", e)

if __name__ == '__main__':
    video_url = get_random_15min_abs_workout()
    if video_url:
        send_telegram_message(video_url)
    else:
        print("No suitable video found.")