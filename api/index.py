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

        "name": "Darkman yt-dlp API",

        "author": "darkman",

        "contact": "t.me/darkman_bin",

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

    }




    if COOKIES_PATH:

        ydl_opts["cookiefile"] = COOKIES_PATH



    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

    except Exception as e:

        return jsonify({"error": str(e)}), 500



    formats = []

    for f in info.get("formats", []):

        formats.append({

            "format_id": f.get("format_id"),

            "ext": f.get("ext"),

            "vcodec": f.get("vcodec"),

            "acodec": f.get("acodec"),

            "resolution": f.get("resolution") or (

                f"{f.get('width')}x{f.get('height')}"

                if f.get("width") and f.get("height") else None

            ),

            "fps": f.get("fps"),

            "filesize": f.get("filesize"),

            "tbr": f.get("tbr"),

            "url": f.get("url"),

        })



    return jsonify({

        "id": info.get("id"),

        "title": info.get("title"),

        "thumbnail": info.get("thumbnail"),

        "duration": info.get("duration"),

        "webpage_url": info.get("webpage_url"),

        "uploader": info.get("uploader"),

        "channel": info.get("channel"),

        "formats": formats,

    })
