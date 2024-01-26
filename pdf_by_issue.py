# pdf_by_issue.py
# create a page-by-page json dump of each issue

import fitz  # PyMuPDF
import sys
import re
import glob
import os
import json

def fix_hyphenation_and_merge_lines(text):
    text = re.sub(r'-\s*\n\s*', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def format_filename(filename):
    base_name, _ = os.path.splitext(filename)
    match = re.match(r"(\d{4})-(\d+)([a-zA-Z]?)", base_name)
    if match:
        year, issue, edition = match.groups()
        formatted_name = f"Skrolli {year}.{issue}"
        if edition:
            formatted_name += edition.upper()
        return formatted_name
    return base_name

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    formatted_filename = format_filename(os.path.basename(pdf_path))

    pages_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        text = fix_hyphenation_and_merge_lines(text)
        pages_text.append({"page": page_num + 1, "content": text})

    doc.close()
    return pages_text

def process_pdf_directory(directory):
    output_dir = os.path.join(directory, 'json_processed')
    os.makedirs(output_dir, exist_ok=True)

    for pdf_file in glob.glob(os.path.join(directory, '*.pdf')):
        pages = extract_text_from_pdf(pdf_file)
        json_data = {
            "issue": format_filename(os.path.basename(pdf_file)),
            "pages": pages
        }

        json_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0] + '.json')
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"Processed {pdf_file} into {json_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_by_issue.py path_to_directory_containing_pdfs")
        sys.exit(1)

    pdf_directory = sys.argv[1]
    process_pdf_directory(pdf_directory)