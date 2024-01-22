# Text parsing with `spacy`
# `pip install spacy` and then your needed packages like:
# `python -m spacy download <your spacy package>`
# i.e. `python -m spacy download fi_core_news_sm`

import spacy
import os
import sys

# Load Finnish spaCy model
nlp = spacy.load("fi_core_news_sm")

def process_file(file_path, output_dir):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        doc = nlp(text)

        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for token in doc:
                output_file.write(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token.dep_}\n')

def process_directory(directory):
    output_dir = os.path.join(directory, 'processed')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming you're processing .txt files
            file_path = os.path.join(directory, filename)
            process_file(file_path, output_dir)
            print(f"Processed {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python spacy_parsing.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    process_directory(directory_path)
