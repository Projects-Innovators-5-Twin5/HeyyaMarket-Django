import cohere

# Initialize the Cohere client
co = cohere.Client('cLd8Vc6TMBoZjfE3bf7FjJCyr2mbYeyP0oZrPuq9')  

def generate_event_descriptioncohere(title, start_datetime, end_datetime, location, available_slots):
    prompt = (f"Create a captivating and detailed event description for a event titled '{title}'. "
              f"This workshop will take place on {start_datetime} to {end_datetime} at {location}, designed for both beginners and enthusiasts. "
              f"There are {available_slots} slots available. "
              f"The description should include what attendees will learn, the benefits of participating, "
              f"exciting activities they can expect, and any unique features that make this event special. "
              f"Make the description engaging, appealing, and at least 150-200 words long, drawing potential participants in.\n")
    
    

    # Generate description
    response = co.generate(
        model='command-r-plus-08-2024', 
        prompt=prompt,
        max_tokens=250, 
        temperature=0.7,  
        stop_sequences=["\n"]
    )

    # Extract and return the generated text
    return response.generations[0].text.strip()
