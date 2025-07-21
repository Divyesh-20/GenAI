from flask import Flask, request, jsonify
import asyncio
from utility.script.script_generator import generate_script  # Must accept (topic, duration)
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url, generate_image_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/generate-video", methods=["POST"])
def generate_video_api():
    try:
        data = request.get_json()

        topic = data.get("topic")
        duration = int(data.get("duration", 60))  # default to 60 if not provided

        if not topic:
            return jsonify({"error": "Missing 'topic' in request body"}), 400

        SAMPLE_FILE_NAME = "audio_tts.wav"
        VIDEO_SERVER = "pexel"

        # 1. Generate script (should now accept duration)
        script = generate_script(topic, duration)

        # 2. Generate audio (async)
        asyncio.run(generate_audio(script, SAMPLE_FILE_NAME))

        # 3. Generate timed captions
        timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)

        # 4. Get video search queries
        search_terms = getVideoSearchQueriesTimed(script, timed_captions)

        # 5. Get background visuals
        background_video_urls = generate_image_url(search_terms, VIDEO_SERVER) if search_terms else None
        background_video_urls = merge_empty_intervals(background_video_urls)

        # 6. Final video output
        if background_video_urls:
            final_video_url = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
            return jsonify({
                "topic": topic,
                "duration": duration,
                "script": script,
                "video_url": final_video_url
            })
        else:
            return jsonify({"error": "No video background found"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, debug=True)
