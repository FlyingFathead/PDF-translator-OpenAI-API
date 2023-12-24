import unicodedata
import shutil
import sys
import os
import re

# print term width horizontal line
def hz_line(character='-'):
    terminal_width = shutil.get_terminal_size().columns
    line = character * terminal_width
    print(line)

""" def sanitize_content(text):
    # Normalize unicode characters to their closest ASCII representation
    text = unicodedata.normalize('NFKC', text)
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n', '', text)
    # Condense all whitespace except for paragraph breaks into a single space
    text = re.sub(r'[^\S\n]+', ' ', text)
    # Replace multiple newlines with a double newline (to preserve paragraph breaks)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text """

""" def sanitize_content(text):
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n\s*', '', text)
    # Replace multiple consecutive spaces with a single space
    text = re.sub(r' {2,}', ' ', text)
    # Ensure that paragraph breaks are maintained
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text """

""" def sanitize_content(text):
    # Normalize unicode characters to their closest ASCII representation
    text = unicodedata.normalize('NFKC', text)
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n', '', text)
    # Replace all whitespace characters (including non-breaking spaces) with a single space
    text = re.sub(r'\s+', ' ', text)
    return text """

# text preprocessing & sanitization
def sanitize_content(text):
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n', '', text)
    # Replace multiple spaces (but not newlines) with a single space
    # text = re.sub(r'[^\S\n]+', ' ', text)
    # text = re.sub(r' {2,}', ' ', text)

    # Replace multiple whitespace characters (including non-breaking spaces) with a single space
    text = re.sub(r'[^\S\r\n]+', ' ', text)    

    # Merge lines into paragraphs
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    text = re.sub(r'[^\S\r\n]+', ' ', text)    
    return text

def split_text_for_translation(file_path, char_limit):
    hz_line()
    print(f"Current character split limit (from next empty line): {char_limit} characters.")
    hz_line()

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Sanitize the text for hyphenation
    content = sanitize_content(content)

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
    num_digits = len(str(len(sections)))  # Calculate the number of digits for formatting

    for i, section in enumerate(sections, start=1):
        formatted_index = str(i).zfill(num_digits)  # Pad the index with leading zeros
        output_filename = os.path.join(output_dir, f"{base_name}_split_{formatted_index}.txt")
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(section)
        print(f"Section {formatted_index} written to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scriptname.py <inputfile>")
        sys.exit(1)

    inputfile = sys.argv[1]
    char_limit = 5000  # Set your character limit here
    main(inputfile, char_limit)