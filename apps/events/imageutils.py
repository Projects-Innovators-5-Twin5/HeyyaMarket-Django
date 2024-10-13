import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_event_image(title, description, location, start_datetime, end_datetime, available_slots,event_type,target_audience,event_theme,level):
    api_key = os.getenv("SECRET_KEY_IMAGE_DESCRIPTION")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Create a prompt for the image
    prompt = (f"A poster for a workshop titled '{title}' at {location}. "
              f"It starts on {start_datetime.strftime('%Y-%m-%d %H:%M')} and ends on {end_datetime.strftime('%Y-%m-%d %H:%M')}. "
              f"{available_slots} slots available. {description}. All text should be in English.")

    data = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True  # Wait for the model to become available if it's currently busy
        }
    }

    # Hugging Face's Stable Diffusion endpoint
    url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # The response includes the base64-encoded image data
        image_data = response.content

        # Save the image to a file
        with open(f"media/events/{title}_generated_image.png", "wb") as f:
            f.write(image_data)

        print("Image generated and saved successfully.")
        return f"{title}_generated_image.png"
    else:
        print(f"Error generating image: {response.text}")
        return None
