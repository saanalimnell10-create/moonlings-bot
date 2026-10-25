from flask import Flask, jsonify, request
from threading import Thread
from urllib.error import HTTPError, URLError
from urllib.request import Request as UrlRequest, urlopen
import json
import os
import re
import secrets

from cogs.welcome import load_settings, update_guild_settings

app = Flask('')

@app.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "private, no-store, max-age=0"
    return response

@app.route('/')
def home():
    return "Moonlings is awake and fluffy! 🌸✨"

def require_control_token():
    expected = os.getenv("BOT_CONTROL_API_TOKEN", "")
    if len(expected) < 32:
        return jsonify(error="Bot control API is not configured."), 503
    scheme, separator, provided = request.headers.get("Authorization", "").partition(" ")
    if not separator or scheme.lower() != "bearer" or not secrets.compare_digest(provided, expected):
        return jsonify(error="Unauthorized."), 401
    return None

def valid_guild_id(guild_id):
    return re.fullmatch(r"\d{17,20}", guild_id) is not None

def fetch_text_channels(guild_id):
    token = os.getenv("DISCORD_TOKEN", "")
    if not token:
        return None, (jsonify(error="Discord bot token is not configured."), 503)
    api_request = UrlRequest(
        f"https://discord.com/api/v10/guilds/{guild_id}/channels",
        headers={"Authorization": f"Bot {token}", "Accept": "application/json"},
    )
    try:
        with urlopen(api_request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code == 404:
            return None, (jsonify(error="Moonlings is not installed in this server."), 404)
        if error.code == 403:
            return None, (jsonify(error="Moonlings cannot view this server's channels."), 403)
        return None, (jsonify(error="Could not load Discord channels."), 502)
    except (URLError, TimeoutError, ValueError):
        return None, (jsonify(error="Could not reach Discord to load channels."), 502)
    if not isinstance(payload, list):
        return None, (jsonify(error="Discord returned an invalid channel list."), 502)
    channels = [
        {"id": channel["id"], "name": channel["name"]}
        for channel in payload
        if isinstance(channel, dict)
        and channel.get("type") in (0, 5)
        and isinstance(channel.get("id"), str)
        and isinstance(channel.get("name"), str)
    ]
    return channels, None

@app.route("/api/admin/guilds/<guild_id>/channels", methods=["GET"])
def admin_guild_channels(guild_id):
    auth_error = require_control_token()
    if auth_error:
        return auth_error
    if not valid_guild_id(guild_id):
        return jsonify(error="Invalid server ID."), 400
    channels, error = fetch_text_channels(guild_id)
    if error:
        return error
    return jsonify(channels=channels)

@app.route("/api/admin/guilds/<guild_id>/welcome", methods=["GET", "PUT"])
def admin_welcome_settings(guild_id):
    auth_error = require_control_token()
    if auth_error:
        return auth_error
    if not valid_guild_id(guild_id):
        return jsonify(error="Invalid server ID."), 400
    if request.method == "GET":
        settings = load_settings()
        data = settings.get(guild_id, {}) if isinstance(settings, dict) else {}
        return jsonify(
            welcomeChannelId=str(data["welcome_channel"]) if data.get("welcome_channel") else None,
            welcomeText=data.get("welcome_text", "Welcome to {server}, {user}! 🎉"),
            goodbyeChannelId=str(data["goodbye_channel"]) if data.get("goodbye_channel") else None,
            goodbyeText=data.get("goodbye_text", "Goodbye, {user}. We'll miss you! 👋"),
        )
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify(error="A JSON settings object is required."), 400
    welcome_channel = body.get("welcomeChannelId")
    goodbye_channel = body.get("goodbyeChannelId")
    welcome_text = body.get("welcomeText")
    goodbye_text = body.get("goodbyeText")
    if not isinstance(welcome_channel, str) or not valid_guild_id(welcome_channel):
        return jsonify(error="Choose a valid welcome text channel."), 400
    if not isinstance(goodbye_channel, str) or not valid_guild_id(goodbye_channel):
        return jsonify(error="Choose a valid goodbye text channel."), 400
    if not isinstance(welcome_text, str) or not welcome_text.strip() or len(welcome_text.strip()) > 1800:
        return jsonify(error="Welcome messages must contain 1 to 1,800 characters."), 400
    if not isinstance(goodbye_text, str) or not goodbye_text.strip() or len(goodbye_text.strip()) > 1800:
        return jsonify(error="Goodbye messages must contain 1 to 1,800 characters."), 400
    channels, error = fetch_text_channels(guild_id)
    if error:
        return error
    channel_ids = {channel["id"] for channel in channels}
    if welcome_channel not in channel_ids or goodbye_channel not in channel_ids:
        return jsonify(error="Choose channels that still belong to this server."), 400
    update_guild_settings(guild_id, {
        "welcome_channel": welcome_channel,
        "welcome_text": welcome_text.strip(),
        "goodbye_channel": goodbye_channel,
        "goodbye_text": goodbye_text.strip(),
    })
    return jsonify(ok=True)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
