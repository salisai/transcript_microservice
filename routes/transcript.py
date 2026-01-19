from flask import Blueprint, request, jsonify 
from services.yt_service import fetch_yt_transcript 
from services.supadata_service import fetch_supadata_transcript 
from utils.errors import TranscriptError 

bp = Blueprint("transcript", __name__)

@bp.route("/transcript", methods=["POST"])
def get_transcript():
    # Validate request content type
    if not request.is_json:
        raise TranscriptError("INVALID_INPUT", "Request must be JSON", 400)
    
    data = request.get_json()
    
    if not data:
        raise TranscriptError("INVALID_INPUT", "Request body is required", 400)
    
    video_id = data.get("video_id")

    if not video_id:
        raise TranscriptError("INVALID_INPUT", "video_id is required", 400)
    
    if not isinstance(video_id, str) or len(video_id.strip()) == 0:
        raise TranscriptError("INVALID_INPUT", "video_id must be a non-empty string", 400)

    # Try YouTube first
    try: 
        transcript = fetch_yt_transcript(video_id.strip())
        source = "youtube"
    except TranscriptError:
        # Re-raise custom errors
        raise

    except Exception as e:
        try: 
            transcript = fetch_supadata_transcript(video_id.strip())
            source = "supadata"
        except TranscriptError:
            raise
            
        except Exception as fallback_error:
            raise TranscriptError(
                "TRANSCRIPT_NOT_FOUND",
                "No transcript is available from any provider we use. Please try another video",
                404
            )
    
    return jsonify({
        "source": source, 
        "transcript": transcript
    }), 200