# Dialogflow Chatbot Python Templates

This folder contains a simple Python scaffold for a Dialogflow chatbot: a Flask webhook for fulfillment, a Dialogflow client helper, an optional Streamlit demo UI, and a Telegram webhook example.

## Quick start

1. Create a Google Cloud project and Dialogflow ES agent.
2. Create a service account with Dialogflow API access and download JSON credentials. Save as `service_account.json` and set:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="$PWD/service_account.json"
   export DIALOGFLOW_PROJECT_ID="your-project-id"
   ```

3. Install dependencies:

   python -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt

4. Run the Flask webhook locally for testing:

   python app.py

   Use ngrok to expose it publicly for Dialogflow fulfillment:

   ngrok http 8080

   Copy the ngrok HTTPS URL and set it as your Fulfillment webhook in Dialogflow.

5. Streamlit demo:

   export DIALOGFLOW_PROJECT_ID="your-project-id"
   streamlit run streamlit_chat.py

6. Telegram integration (optional):

   - Create a bot with BotFather and obtain `TELEGRAM_BOT_TOKEN`.
   - Run `telegram_bot.py` as public HTTPS service and set Telegram webhook to `https://<your-url>/telegram_webhook`.

## Files
- `dialogflow_client.py` — helper to call Dialogflow detectIntent
- `app.py` — minimal Flask webhook for Dialogflow fulfillment
- `streamlit_chat.py` — Streamlit chat UI demo
- `telegram_bot.py` — minimal Telegram webhook forwarder
- `sample_intents.json` — example intents & training phrases

## Notes
- Dialogflow import format is more complex; use the Dialogflow console to create intents and entities or use the API/CLI if you prefer automation.
- For production, validate and secure your endpoints, add authentication, and use HTTPS with a valid cert.
