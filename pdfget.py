# pdfget.py

import fitz  # PyMuPDF
import sys
import re
import glob
import os

def extract_text_from_pdf(pdf_path):
    # Extract text from each page of the PDF.
    # Include markers between each page in the format: === [ filename_without_extension | pagenumber / total pages] ===
    
    doc = fitz.open(pdf_path)
    extracted_text = ""
    total_pages = len(doc)
    filename_without_extension = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        text = page.get_text()

        # Add marker before the page text
        page_marker = f"\n\n=== [ {filename_without_extension} | {page_num + 1}/{total_pages} ] ===\n\n"
        extracted_text += page_marker + text

    doc.close()
    return extracted_text

def process_pdf_directory(directory):
    output_dir = os.path.join(directory, 'txt_raw')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pdf_file in glob.glob(os.path.join(directory, '*.pdf')):
        text = extract_text_from_pdf(pdf_file)
        txt_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0] + '.txt')
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(text)
        print(f"Processed {pdf_file} into {txt_filename}")

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py path_to_directory_containing_pdfs")
        sys.exit(1)

    pdf_directory = sys.argv[1]
    process_pdf_directory(pdf_directory)


## below is the old verison
""" # old version, w/ parsing: pdfget.py

import fitz  # PyMuPDF
import sys
import re
import glob
import os

def extract_text_from_pdf(pdf_path):

    # Extract text from each page of the PDF and attempt to maintain natural reading order.
    # Also, handle line continuation hyphenations.

    doc = fitz.open(pdf_path)
    extracted_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")  # Extract text blocks

        # Sort blocks based on their position: top to bottom, left to right
        blocks.sort(key=lambda b: (b[1], b[0]))

        for b in blocks:
            block_text = b[4].strip()
            if block_text:  # Exclude empty blocks
                extracted_text += block_text + "\n"

        extracted_text += "\n\n"  # Add a gap between pages

    doc.close()

    # Handle continuation hyphenations
    def fix_hyphenation(match):
        return match.group(1) + match.group(2)

    hyphenated_word_pattern = re.compile(r'(\w+)-\s+(\w+)')
    extracted_text = re.sub(hyphenated_word_pattern, fix_hyphenation, extracted_text)

    return extracted_text

def process_pdf_directory(directory):
    for pdf_file in glob.glob(os.path.join(directory, '*.pdf')):
        text = extract_text_from_pdf(pdf_file)
        txt_filename = pdf_file.rsplit('.', 1)[0] + '.txt'  # Change the extension to .txt
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(text)
        print(f"Processed {pdf_file} into {txt_filename}")

# Main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py path_to_directory_containing_pdfs")
        sys.exit(1)

    pdf_directory = sys.argv[1]
    process_pdf_directory(pdf_directory) """