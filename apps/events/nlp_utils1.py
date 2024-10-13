import cohere
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Cohere client
co = cohere.Client('SECRET_KEY_COHERE')

def generate_event_descriptioncohere(title, start_datetime, end_datetime, location, available_slots, event_type, target_audience, event_theme, level):
    prompt = (f"Create a captivating and detailed event description for an event titled '{title}'. "
              f"This workshop will take place from {start_datetime} to {end_datetime} at {location}, designed for both beginners and enthusiasts. "
              f"There are {available_slots} slots available. "
              f"Make sure the description is at least 150-200 words long and clearly explains what attendees will learn, "
              f"the benefits of participating, exciting activities they can expect, and any unique features that make this event special. "
              f"The description should be engaging and appealing, drawing potential participants in.\n")

    # Generate description
    response = co.generate(
        model='command-r-plus-08-2024', 
        prompt=prompt,
        max_tokens=1000,  # Increase tokens to allow a longer response
        temperature=0.7  # Balance creativity and coherence
    )

    # Extract and return the generated text
    return response.generations[0].text.strip()
