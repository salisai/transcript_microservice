from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    TooManyRequests,
    YouTubeRequestFailed
)
from utils.errors import TranscriptError

def fetch_yt_transcript(video_id):
    """
    Fetches transcript from YouTube using the video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        list: List of transcript segments with text and start time
        
    Raises:
        TranscriptError: If transcript cannot be fetched
    """
    if not video_id or not isinstance(video_id, str):
        raise TranscriptError("INVALID_INPUT", "Invalid video_id provided", 400)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        if not transcript:
            raise TranscriptError(
                "TRANSCRIPT_NOT_FOUND",
                "No transcript available for this video",
                404
            )
        
        # Normalize transcript format
        normalized_transcript = [
            {
                "text": item.get("text", ""),
                "start": float(item.get("start", 0))
            }
            for item in transcript
        ]
        
        return normalized_transcript
        
    except TranscriptsDisabled:
        raise TranscriptError(
            "TRANSCRIPT_DISABLED",
            "Transcripts are disabled for this video",
            404
        )
    except NoTranscriptFound:
        raise TranscriptError(
            "TRANSCRIPT_NOT_FOUND",
            "No transcript found for this video",
            404
        )
    except VideoUnavailable:
        raise TranscriptError(
            "VIDEO_UNAVAILABLE",
            "Video is unavailable or does not exist",
            404
        )
    except TooManyRequests:
        raise TranscriptError(
            "RATE_LIMIT_EXCEEDED",
            "Too many requests. Please try again later",
            429
        )
    except YouTubeRequestFailed as e:
        raise TranscriptError(
            "YOUTUBE_API_ERROR",
            f"YouTube API request failed: {str(e)}",
            500
        )
    except Exception as e:
        raise TranscriptError(
            "TRANSCRIPT_FETCH_ERROR",
            f"Failed to fetch transcript: {str(e)}",
            500
        )