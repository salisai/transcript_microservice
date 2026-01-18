from supadata import Supadata 
from config import Config 

supadata = Supadata(api_key=Config.SUPADATA_API_KEY)

def fetch_supadata_transcript(video_id):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    result = supadata.transcript(
        url=youtube_url,
        lang="en",
        text=False, 
        mode="auto"
    )

    return [
        {
            "text": seg["text"],
            "start": seg["start"]
        }
        for seg in result["segments"]
    ]