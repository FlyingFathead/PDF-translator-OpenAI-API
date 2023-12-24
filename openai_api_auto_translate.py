# PDF-translator-OpenAI-API
# https://github.com/FlyingFathead/PDF-translator-OpenAI-API/
# FlyingFathead // Dec 2023
# v0.03

import sys
import os
import shutil
import configparser

import openai
from transformers import GPT2Tokenizer

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
def count_tokens(file_path):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    max_length = tokenizer.model_max_length  # Get the max length supported by the tokenizer

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the text into smaller chunks
        tokens_count = 0
        start = 0
        while start < len(text):
            end = start + max_length
            chunk = text[start:end]
            tokens = tokenizer.encode(chunk, add_special_tokens=False)  # Do not add special tokens for each chunk
            tokens_count += len(tokens)
            start = end

        return tokens_count
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def translate_text(text, model, instructions):
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=f"{instructions}: '{text}'",
            max_tokens=32000  # Adjust as needed
        )
        return response.choices[0].text.strip()
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
def main(directory, model, char_limit, instructions):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"Directory {directory} does not exist or is not a directory.")
        sys.exit(1)

    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    if not text_files:
        print(f"No text files found in directory {directory}.")
        sys.exit(1)

    total_tokens = 0
    print("Calculating token counts for files...", flush=True)
    for file in text_files:
        file_path = os.path.join(directory, file)
        token_count = count_tokens(file_path)
        if token_count is not None:
            total_tokens += token_count

    hz_line()
    print(f"Directory: {directory}")
    print(f"Number of text files: {len(text_files)}")
    print(f"Combined length: {total_tokens} tokens")
    print(f"Instructions to the model: {instructions}")  # Use instructions from config
    print(f"Model in use: {model}")
    hz_line()

    confirm = input("Do you wish to continue (y/n)? ")
    if confirm.lower() != 'y':
        print("Translation cancelled.")
        sys.exit(0)

    for file in text_files:
        file_path = os.path.join(directory, file)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = f"{directory}/{base_name}-translations"
        os.makedirs(output_dir, exist_ok=True)

        print(f"Processing file: {file}", flush=True)
        sections = split_text_for_translation(file_path, char_limit)
        num_digits = len(str(len(sections)))

        for i, section in enumerate(sections, start=1):
            hz_line()
            print(f"Translating segment: {i}/{len(sections)} of file {file}", flush=True)
            hz_line()

            translated_section = translate_text(section, model, instructions)
            if translated_section:
                formatted_index = str(i).zfill(num_digits)
                output_filename = os.path.join(output_dir, f"{base_name}_translated_split_{formatted_index}.txt")
                with open(output_filename, 'w', encoding='utf-8') as output_file:
                    output_file.write(translated_section)
                print(f"Translated section {formatted_index} written to {output_filename}", flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python openai_api_auto_translate.py <directory>")
        sys.exit(1)

    # Extracting configuration settings
    config = load_config()
    directory = sys.argv[1]
    char_limit = int(config.get('MaxCharacterLimit', 100000))
    model = config.get('Model', 'gpt-3.5-turbo')
    instructions = config.get('TranslationInstructions', 'Translate this Finnish text to English, format the text properly')

    # Call main with the instructions parameter
    main(directory, model=model, char_limit=char_limit, instructions=instructions)
