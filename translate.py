import shutil
import sys
import os
import openai

# print term width horizontal line
def hz_line(character='-'):
    terminal_width = shutil.get_terminal_size().columns
    line = character * terminal_width
    print(line)

# API key reading
# First, try to get the API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# If the environment variable is not set, try to read the key from a file
if openai.api_key is None:
    try:
        with open('api_token.txt', 'r') as file:
            openai.api_key = file.read().strip()
    except FileNotFoundError:
        print("Error: The OPENAI_API_KEY environment variable is not set, and api_token.txt was not found. Please set the environment variable or create this file with your OpenAI API key.")
        sys.exit(1)

# If the key is still None at this point, neither method was successful
if openai.api_key is None:
    print("Error: Failed to obtain OpenAI API key. Please set the OPENAI_API_KEY environment variable or create a file named api_token.txt with your OpenAI API key.")
    sys.exit(1)

def translate_text(text, model="gpt-3.5-turbo"):
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=f"Translate this Finnish text to English: '{text}'",
            max_tokens=1000  # Adjust as needed
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

# Example usage for a chunk of text
# translated_text = translate_text("Your chunk of text here")
# print(translated_text) """