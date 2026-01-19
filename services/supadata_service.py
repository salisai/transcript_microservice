from supadata import Supadata 
from config import Config 
from utils.errors import TranscriptError

# Initialize SupaData client only if API key is available
supadata = None
if Config.SUPADATA_API_KEY:
    try:
        supadata = Supadata(api_key=Config.SUPADATA_API_KEY)
    except Exception as e:
        #service can still work with YouTube only
        print(f"Warning: Failed to initialize SupaData client: {str(e)}")


def fetch_supadata_transcript(video_id):
    """
    Fetches transcript from SupaData API using the video ID.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        list: List of transcript segments with text and start time
        
    Raises:
        TranscriptError: If transcript cannot be fetched or API key is missing
    """
    if not supadata:
        raise TranscriptError(
            "SUPADATA_NOT_CONFIGURED",
            "SupaData API key is not configured",
            500
        )
    
    if not video_id or not isinstance(video_id, str):
        raise TranscriptError("INVALID_INPUT", "Invalid video_id provided", 400)
    
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        result = supadata.transcript(
            url=youtube_url,
            lang="en",
            text=False, 
            mode="auto"
        )
        
        if not result or "segments" not in result:
            raise TranscriptError(
                "TRANSCRIPT_NOT_FOUND",
                "No transcript segments found in SupaData response",
                404
            )
        
        # Normalize transcript format
        normalized_transcript = [
            {
                "text": seg.get("text", ""),
                "start": float(seg.get("start", 0))
            }
            for seg in result["segments"]
            if isinstance(seg, dict) and "text" in seg and "start" in seg
        ]
        
        if not normalized_transcript:
            raise TranscriptError(
                "TRANSCRIPT_NOT_FOUND",
                "No valid transcript segments found",
                404
            )
        
        return normalized_transcript
        
    except TranscriptError:
        # Re-raise custom errors
        raise
        
    except Exception as e:
        raise TranscriptError(
            "SUPADATA_API_ERROR",
            f"Failed to fetch transcript from SupaData: {str(e)}",
            500
        )