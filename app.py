import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")
API = "https://najmi-ob53-like-api-vvkb.vercel.app/like"
KEY = os.environ.get("LIKE_API_KEY", "NJM")


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.get("/like")
def like():
    uid = request.args.get("uid", "").strip()
    region = request.args.get("server_name", "").strip().lower()
    if not uid.isdigit() or not (5 <= len(uid) <= 15) or not region.isalpha():
        return jsonify(error="Invalid uid or region"), 400
    try:
        r = requests.get(API, params={"uid": uid, "server_name": region, "key": KEY}, timeout=25)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify(error=str(e)), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
