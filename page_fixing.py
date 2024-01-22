# page_fixing.py

import re
import os
import sys

# Remove control characters
def remove_control_characters(text):
    return re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)

def parse_text(text):
    # Split text by custom page markers and keep the markers with empty lines before and after
    pages = re.split(r"(=== \[\s*\d{4}-\d\s*\|\s*\d+/\d+\s*\] ===)", text)

    # Process each page while retaining the markers with the required empty lines
    processed_text = ""
    for section in pages:
        if section.strip():
            # Add empty lines around markers
            if section.startswith("==="):
                processed_text += "\n" + section + "\n"
            else:
                processed_text += process_page(section)
    return processed_text

def process_page(page_text):
    # Handle line continuations and hyphenations
    page_text = re.sub(r'-\s*\n', '', page_text)
    # Normalize spaces (including newlines)
    page_text = re.sub(r'\s+', ' ', page_text).strip()
    # Remove control characters
    page_text = remove_control_characters(page_text)
    return page_text + "\n"

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python page_fixing.py path_to_directory_containing_txt_files")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = os.path.join(input_directory, 'txt_processed')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_directory, filename)
            with open(input_file_path, 'r') as file:
                text = file.read()
                processed_text = parse_text(text)

            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, 'w') as file:
                file.write(processed_text)
            print(f"Processed {filename} into {output_file_path}")