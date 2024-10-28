from transformers import pipeline

def generate_event_description(title, start_datetime, end_datetime , location, available_slots ):
    generator = pipeline('text-generation', model='gpt2')

    # Improved prompt with more context
    prompt = (f"Event: {title}\n"
              f"Start Date: {start_datetime}\n"
              f"End Date: {end_datetime}\n"
              f"Location: {location}\n"
              f"Available slots: {available_slots}\n"
              f"Description:")

    # Generate a description
    result = generator(prompt, max_length=150, num_return_sequences=1, truncation=True, pad_token_id=generator.tokenizer.eos_token_id)

    # Extract the generated text
    generated_text = result[0]['generated_text']

    # Return the description after the prompt
    description = generated_text.split("Description:")[-1].strip()
    return description
