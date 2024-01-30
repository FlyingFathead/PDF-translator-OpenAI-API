import os
import sys
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import glob

# Define your chunk sizes and overlap here
CHUNK_SIZE = 1024
CHUNK_OVERLAP = 100

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def split_text_with_recursive_splitter(text, chunk_size=1024, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_text(text)

def vectorize_chunks(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return [model.encode(chunk) for chunk in chunks]

def process_file(file_path):
    print(f"Processing file: {file_path}")
    json_data = load_json_data(file_path)
    all_vectorized_chunks = []
    for page in json_data['pages']:
        chunks = split_text_with_recursive_splitter(page['content'])
        vectorized_chunks = vectorize_chunks(chunks)
        # Store these vectorized chunks in Redis or handle them as needed
        all_vectorized_chunks.extend(vectorized_chunks)
    # Process the vectorized chunks further as needed

def process_directory(directory_path):
    for file_path in glob.glob(os.path.join(directory_path, '*.json')):
        process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path to JSON file or directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    if os.path.isfile(input_path):
        process_file(input_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    else:
        print("Invalid path. Please provide a valid JSON file or directory path.")
        sys.exit(1)
