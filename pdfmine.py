# requires `pdfminer.six`; install with `pip install -U pdfminer.six`

import sys
import os
from pdfminer.high_level import extract_text

def extract_pdf_text(pdf_file, output_file):
    if os.path.exists(output_file):
        print(f"File {output_file} already exists. Aborting to prevent overwriting.")
        return False
    try:
        print(f"Extracting text from PDF source file: {inputfile} ...", flush=True)
        text = extract_text(pdf_file)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: pdfmine.py <inputfile>")
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = os.path.splitext(inputfile)[0] + '.txt'
    success = extract_pdf_text(inputfile, outputfile)
    
    if success:
        print(f"Text extracted successfully to {outputfile}")
