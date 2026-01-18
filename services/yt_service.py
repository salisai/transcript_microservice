from youtube_transcript_api import YouTubeTranscriptApi

def fetch_yt_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    return [
        {
            "text": item["text"],
            "start": item["start"]
        }
        for item in transcript
    ]