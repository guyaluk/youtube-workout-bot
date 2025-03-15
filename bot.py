import random
import requests
from youtubesearchpython import VideosSearch

def get_random_15min_abs_workout():
    query = "15 minute abs workout"
    videos_search = VideosSearch(query, limit=20)
    results = videos_search.result()["result"]
    
    # Filter videos: only include those that are roughly 15 minutes long (e.g., 14 to 16 minutes)
    filtered_videos = []
    for video in results:
        duration_str = video.get("duration")
        if duration_str and ":" in duration_str:
            parts = duration_str.split(':')
            seconds = sum(int(x) * (60 ** (len(parts)-i-1)) for i, x in enumerate(parts))
            # Check if duration is between 14 and 16 minutes
            if 14 * 60 <= seconds <= 16 * 60:
                filtered_videos.append(video)
    
    if not filtered_videos:
        return None
    
    # Select a random video from the filtered list
    video = random.choice(filtered_videos)
    return video["link"]

def send_whatsapp_message(video_url):
    # Replace these with your actual CallMeBot API key and WhatsApp group ID
    api_key = "YOUR_CALLMEBOT_API_KEY"
    group_id = "YOUR_WHATSAPP_GROUP_ID"
    
    message = f"Good morning! Here’s your 15-minute abs workout for today: {video_url}"
    # Construct the CallMeBot API URL (consult CallMeBot docs for the correct endpoint and parameters)
    url = f"https://api.callmebot.com/whatsapp.php?apikey={api_key}&text={message}&groupid={group_id}"
    
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    video_url = get_random_15min_abs_workout()
    if video_url:
        result = send_whatsapp_message(video_url)
        print("Message sent:", result)
    else:
        print("No suitable video found.")
