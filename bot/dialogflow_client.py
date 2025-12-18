"""Helper functions to call Dialogflow Detect Intent API using google-cloud-dialogflow."""
from google.cloud import dialogflow_v2 as dialogflow
import uuid


def detect_intent_text(project_id: str, text: str, session_id: str = None, language_code: str = "en") -> dict:
    """Send text to Dialogflow and return the full response (dict).

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set to a service account JSON with Dialogflow access.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return {
        "query_text": response.query_result.query_text,
        "intent": response.query_result.intent.display_name if response.query_result.intent else None,
        "confidence": response.query_result.intent_detection_confidence,
        "parameters": dict(response.query_result.parameters),
        "fulfillment_text": response.query_result.fulfillment_text,
        "raw_response": response,
    }


if __name__ == "__main__":
    import os
    project_id = os.environ.get("DIALOGFLOW_PROJECT_ID")
    if not project_id:
        print("Set DIALOGFLOW_PROJECT_ID environment variable to test")
    else:
        print(detect_intent_text(project_id, "Where is my order?"))
