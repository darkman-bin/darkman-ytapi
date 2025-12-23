import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

COOKIES_ENV_VAR = "YTDLP_COOKIES"
COOKIES_PATH = None

cookies_text = os.getenv(COOKIES_ENV_VAR)
if cookies_text:
    tmp_dir = os.getenv("TMPDIR", "/tmp")
    COOKIES_PATH = os.path.join(tmp_dir, "cookies.txt")
    try:
        with open(COOKIES_PATH, "w", encoding="utf-8") as f:
            f.write(cookies_text)
    except OSError:
        COOKIES_PATH = None

@app.get("/")
def root():
    return jsonify({
        "status": "ok",
        "cookies_loaded": bool(COOKIES_PATH),
    })

@app.get("/info")
def video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url parameter required"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    if COOKIES_PATH:
        ydl_opts["cookiefile"] = COOKIES_PATH

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    video_formats = []
    audio_formats = []

    for f in info.get("formats", []):
        if not f.get("url"):
            continue

        format_data = {
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "resolution": f.get("resolution") or "unknown",
            "filesize": f.get("filesize"),
            "url": f.get("url"),
            "note": f.get("format_note"),
            "vcodec": f.get("vcodec"),
            "acodec": f.get("acodec"),
        }

        vcodec = f.get("vcodec", "none")
        acodec = f.get("acodec", "none")

        if vcodec == "none" and acodec != "none":
            audio_formats.append(format_data)
        elif vcodec != "none":
            video_formats.append(format_data)

    video_formats.reverse()
    audio_formats.reverse()

    return jsonify({
        "id": info.get("id"),
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "video_formats": video_formats,
        "audio_formats": audio_formats,
    })
