import sys
import os
import shutil
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
            prompt=f"Translate this Finnish text to English, sanitize hyphenation: '{text}'",
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

def main(file_path, char_limit):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = f"{base_name}-splits"
    os.makedirs(output_dir, exist_ok=True)

    sections = split_text_for_translation(file_path, char_limit)
    num_digits = len(str(len(sections)))

    for i, section in enumerate(sections, start=1):
        hz_line()
        print(f"Translating segment: {i}/{len(sections)}")
        hz_line()
        print("[INPUT]\n")
        print(section)
        hz_line()
        print("[OUTPUT]\n")

        translated_section = translate_text(section)
        if translated_section:
            print(translated_section)
            hz_line()

            formatted_index = str(i).zfill(num_digits)
            output_filename = os.path.join(output_dir, f"{base_name}_translated_split_{formatted_index}.txt")
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(translated_section)
            print(f"Translated section {formatted_index} written to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scriptname.py <inputfile>")
        sys.exit(1)

    inputfile = sys.argv[1]
    char_limit = 5000  # Adjust character limit as needed
    main(inputfile, char_limit)