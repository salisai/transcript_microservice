from flask import Blueprint, request, jsonify 
from services.yt_service import fetch_yt_transcript 
from services.supadata_service import fetch_supadata_transcript 
from utils.errors import Transcripter 

bp = Blueprint("transcript", __name__)

@bp.route("/transcript", methods=["POST"])
def get_transcript():
    data = request.get_json()
    video_id = data.get("video_id")

    if not video_id:
        raise Transcripter("INVALID_INPUT", "video id is required")

    try: 
        transcript = fetch_yt_transcript(video_id)
        source = "youtube"
    except Exception:
        try: 
            transcript = fetch_supadata_transcript(video_id)
            source = "supadata"
        except Exception: 
            raise Transcripter(
                "TRANSCRIPT_NOT_FOUND",
                "No transcript is available from any provider we use. Please try another video"
            )
    
    return jsonify({
        "source": source, 
        "transcript": transcript
    })