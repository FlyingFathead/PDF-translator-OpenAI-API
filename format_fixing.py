# format_fixing.py
import os
import sys
import re

def clean_text(text):
    # Correct hyphenated words at line breaks
    text = re.sub(r'-\s*\n', '', text)
    # Normalize spaces and remove multiple consecutive spaces
    text = re.sub(r' +', ' ', text)
    # Remove unnecessary single newlines within paragraphs, preserve multiple newlines (paragraph breaks)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Additional step to trim multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    return text

def process_file(file_path, output_dir):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        cleaned_text = clean_text(text)

        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(cleaned_text)

def process_directory(directory):
    output_dir = os.path.join(directory, 'cleaned')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            process_file(file_path, output_dir)
            print(f"Cleaned {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_fixing.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    process_directory(directory_path)