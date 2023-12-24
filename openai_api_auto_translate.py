# PDF-translator-OpenAI-API
# https://github.com/FlyingFathead/PDF-translator-OpenAI-API/
#
# FlyingFathead // Dec 2023
# v0.09
#
# changelog:
# v0.09 - token handling, naming policy
# v0.08 - more changes to the API call functionality
# v0.07 - API call updated and fixed for openai >v1.0
# v0.06 - fixes to the API call
# v0.05 - calculate the cost approximation
# v0.04 - calculate both tokens and chars

import sys
import os
import shutil
import configparser

import openai
from transformers import GPT2Tokenizer

from openai_pricing_calculator import calculate_cost

# print term width horizontal line
def hz_line(character='-'):
    terminal_width = shutil.get_terminal_size().columns
    line = character * terminal_width
    print(line)

# laod the config
def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']

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

# count the tokens
def count_tokens_and_chars(file_path):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    max_length = tokenizer.model_max_length

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        tokens_count = 0
        chars_count = 0  # Initialize character count
        start = 0
        while start < len(text):
            end = start + max_length
            chunk = text[start:end]
            tokens = tokenizer.encode(chunk, add_special_tokens=False)
            tokens_count += len(tokens)
            chars_count += len(chunk)  # Count characters in the chunk
            start = end

        return tokens_count, chars_count
    except Exception as e:
        print(f"Error processing file: {e}")
        return None, None  # Return None for both counts in case of an error

# text translation via OpenAI API
def translate_text(text, model, instructions, max_allowed_tokens):
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Tokenize the input text to estimate its length
    input_tokens = len(text.split())  # This is a rough estimation

    # Adjust max_tokens to avoid exceeding the model's limit
    max_tokens = max_allowed_tokens - input_tokens

    # Ensure max_tokens is positive and within a reasonable range
    max_tokens = max(1, min(max_tokens, max_allowed_tokens))

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"{instructions}"},
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens
        )
        # Access the completion using the appropriate method
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return None
    
def split_text_for_translation(file_path, char_limit):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = []
    current_section = ""
    for line in content.split('\n'):
        if len(current_section) + len(line) < char_limit or not line.strip():
            current_section += line + '\n'
        else:
            sections.append(current_section)
            current_section = line + '\n'
    if current_section:
        sections.append(current_section)

    return sections

# def main(file_path, char_limit):
def main(directory, model, char_limit, instructions, max_tokens):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"Directory {directory} does not exist or is not a directory.")
        sys.exit(1)

    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not text_files:
        print(f"No text files found in directory {directory}.")
        sys.exit(1)

    total_tokens = 0
    total_chars = 0  # Total character count

    print("Calculating token and character counts for files...", flush=True)
    for file in text_files:
        file_path = os.path.join(directory, file)
        token_count, char_count = count_tokens_and_chars(file_path)
        if token_count is not None and char_count is not None:
            total_tokens += token_count
            total_chars += char_count  # Sum character counts

    hz_line()
    print(f"::: Directory: {directory}")
    print(f"::: Number of text files: {len(text_files)}")
    print(f"::: Combined token length: {total_tokens} tokens")
    print(f"::: Combined character length: {total_chars} characters")  # Display total characters
    print(f"::: Instructions to the model: {instructions}")
    print(f"::: Model in use: {model}")

    # Calculate and display cost
    # Assuming output token count is approximately equal to input token count
    input_token_count = total_tokens
    output_token_count = total_tokens  # Approximation

    # Calculate and display cost
    try:
        cost = calculate_cost(model, input_token_count, output_token_count)
        print(f"::: Estimated cost for translation: ${cost:.4f}")
    except ValueError as e:
        print(f"Error in cost calculation: {e}")

    hz_line()

    confirm = input("Do you wish to continue (y/n)? ")
    if confirm.lower() != 'y':
        print("Translation cancelled.")
        sys.exit(0)

    for file in text_files:
        file_path = os.path.join(directory, file)
        base_name, file_extension = os.path.splitext(file)
        output_filename = os.path.join(directory, f"translated_{base_name}{file_extension}")

        print(f"Processing file: {file}", flush=True)
        sections = split_text_for_translation(file_path, char_limit)

        translated_content = ""  # Initialize an empty string to accumulate translated sections
        for i, section in enumerate(sections, start=1):
            hz_line()
            print(f"::: Translating segment: {i}/{len(sections)} of file {file}", flush=True)
            hz_line()

            translated_section = translate_text(section, model, instructions, max_tokens)
            if translated_section:
                translated_content += translated_section  # Append each translated section

        # Write all translated content to a single file
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(translated_content)
        print(f"Translated file written to {output_filename}", flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python openai_api_auto_translate.py <directory>")
        sys.exit(1)

    # Extracting configuration settings
    config = load_config()
    directory = sys.argv[1]
    char_limit = int(config.get('MaxCharacterLimit', 100000))
    max_tokens = int(config.get('MaxTokens', 16000))  # Default to 16000 if not set
    model = config.get('Model', 'gpt-3.5-turbo')
    instructions = config.get('TranslationInstructions', 'Translate this Finnish text to English, format the text properly')

    # Call main with the necessary parameters
    main(directory, model=model, char_limit=char_limit, instructions=instructions, max_tokens=max_tokens)