import os
from google.cloud import dialogflow

from google.api_core.exceptions import InvalidArgument

# Charger les identifiants du fichier JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/keys/dialogflow-service-account.json"

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return response.query_result.fulfillment_text
