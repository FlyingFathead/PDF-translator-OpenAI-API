from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTTextContainer

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

# text preprocessing & sanitization

""" def sanitize_content(text):
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n', '', text)
    
    # Replace multiple whitespace characters with a single space
    text = re.sub(r'[^\S\r\n]+', ' ', text)

    # Treat two or more newline characters as paragraph breaks
    text = re.sub(r'\n{2,}', '\n\n', text)

    # Replace single newlines with spaces (assuming they are not paragraph breaks)
    text = re.sub(r'\n', ' ', text)

    return text """

def sanitize_content(text):
    # Remove hyphenation at the end of lines and join words
    text = re.sub(r'-\s*\n', '', text)
    # Replace multiple spaces (but not newlines) with a single space
    # text = re.sub(r'[^\S\n]+', ' ', text)
    # text = re.sub(r' {2,}', ' ', text)

    # Replace multiple whitespace characters (including non-breaking spaces) with a single space
    text = re.sub(r'[^\S\r\n]+', ' ', text)    

    # Merge lines into paragraphs
    # text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Add another whitespace catcher step
    # text = re.sub(r'[^\S\r\n]+', ' ', text)    
    
    return text

# Extract all text from the PDF.
# Renamed function to avoid conflict with pdfminer's extract_text
def extract_full_text(pdf_file):
    text_content = ''
    for page_layout in extract_pages(pdf_file):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_content += element.get_text()
    return text_content

def extract_text_by_page(pdf_file):
    page_texts = []
    for page_layout in extract_pages(pdf_file):
        page_text = ''
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        page_texts.append(sanitize_content(page_text))
    return page_texts

def split_text_by_char_limit(text, char_limit):
    hz_line()
    print(f"Current character split limit (from next empty line): {char_limit} characters.", flush=True)
    hz_line()

    # Sanitize the text for hyphenation
    text = sanitize_content(text)  # Corrected from 'content' to 'text'

    sections = []
    current_section = ""
    for line in text.split('\n'):  # Corrected from 'content' to 'text'
        if len(current_section) + len(line) < char_limit or not line.strip():
            current_section += line + '\n'
        else:
            sections.append(current_section)
            current_section = line + '\n'
    if current_section:
        sections.append(current_section)

    return sections

# Write sections to files in the output directory.
def write_sections_to_files(sections, base_name, output_dir):
    num_digits = len(str(len(sections)))  # Calculate the number of digits for formatting
    for i, section in enumerate(sections, start=1):
        formatted_index = str(i).zfill(num_digits)  # Pad the index with leading zeros
        output_filename = os.path.join(output_dir, f"{base_name}_split_{formatted_index}.txt")
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(section)
        print(f"Section {formatted_index} written to {output_filename}")

def main(pdf_file, split_by='page', char_limit=5000):
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_dir = f"{base_name}-splits"
    os.makedirs(output_dir, exist_ok=True)

    # Start processing message
    hz_line()
    print(f"::: Extracting from: {pdf_file}", flush=True)
    print(f"::: Mode: {'Split by page' if split_by == 'page' else 'Split by chars'}", flush=True)
    sys.stdout.flush()  # Explicitly flush the output buffer
    hz_line()
    sys.stdout.flush()  # Explicitly flush the output buffer

    if split_by == 'page':
        sections = extract_text_by_page(pdf_file)
    else:
        full_text = extract_full_text(pdf_file)  # Renamed function call
        full_text = sanitize_content(full_text)
        sections = split_text_by_char_limit(full_text, char_limit)

    write_sections_to_files(sections, base_name, output_dir)

if __name__ == "__main__":
    split_method = 'page'  # Default split method
    char_limit = 5000  # Default character limit
    if len(sys.argv) < 2:
        print("Usage: python pdf_extract_and_split.py <inputfile.pdf> [split_method] [char_limit]")
        sys.exit(1)

    inputfile = sys.argv[1]
    if len(sys.argv) >= 3:
        split_method = sys.argv[2]
    if len(sys.argv) == 4:
        char_limit = int(sys.argv[3])

    main(inputfile, split_method, char_limit)
