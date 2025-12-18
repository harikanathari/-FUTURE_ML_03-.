"""Minimal Telegram webhook handler that forwards messages to Dialogflow and replies.

Set env vars: TELEGRAM_BOT_TOKEN, DIALOGFLOW_PROJECT_ID
Use a public HTTPS URL (Cloud Run / ngrok) and register it with Telegram's setWebhook.
"""
import os
import requests
from flask import Flask, request, jsonify
from dialogflow_client import detect_intent_text

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID")

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True)
    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify({"ok": True})

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    # Send to Dialogflow
    res = detect_intent_text(PROJECT_ID, text)
    reply = res.get("fulfillment_text") or "Sorry, I didn't understand."

    # Send reply back to Telegram
    requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": reply})
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
