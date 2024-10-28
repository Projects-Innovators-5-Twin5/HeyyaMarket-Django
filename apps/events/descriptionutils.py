import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def generate_event_descriptionhug(title, start_datetime, end_datetime, location, available_slots, event_type, target_audience, event_theme, level):
    api_key = os.getenv("SECRET_KEY_IMAGE_DESCRIPTION")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Enhanced prompt using the additional fields
    prompt = (f"Join us for a {', '.join(event_type)} titled '{title}', tailored for {', '.join(target_audience)}. "
              f"The event will focus on {', '.join(event_theme)} and is suitable for {', '.join(level)} participants. "
              f"It will take place at {location} from {start_datetime.strftime('%Y-%m-%d %H:%M')} "
              f"to {end_datetime.strftime('%Y-%m-%d %H:%M')}. "
              f"There are {available_slots} slots available, so don't miss out!")

    data = {
        "inputs": prompt,
        "options": {
            "max_length": 250,  # Longer to allow detailed responses
            "wait_for_model": True
        }
    }

    # Hugging Face's text-generation endpoint
    url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        return generated_text.strip()
    else:
        print(f"Error generating description: {response.text}")
        return None
