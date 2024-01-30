# rag_redis_process.py

import os
import sys
import json
import glob
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Redis
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document  # Import Document class
from rag_redis.config import EMBED_MODEL, INDEX_NAME, INDEX_SCHEMA, REDIS_URL

""" REDIS_URL = "redis://localhost:6379"
INDEX_NAME = "skrolli_index"
INDEX_SCHEMA = {
    'text': [{'name': 'content'}],
    'vector': [{'name': 'content_vector', 'algorithm': 'HNSW', 'datatype': 'FLOAT32', 'dims': 384, 'distance_metric': 'COSINE'}]
}
 """
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def vectorize_text(text):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model.encode(text)

def process_file(file_path):
    print(f"Processing file: {file_path}")
    json_data = load_json_data(file_path)
    documents = []
    for page in json_data['pages']:
        vectorized_chunk = vectorize_text(page['content'])
        document = Document(
            page_content=page['content'],
            metadata={"page": page.get("page"), "issue": json_data.get("issue")}
        )
        documents.append(document)

    embedder = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    redis_store = Redis(embedding=embedder, index_name=INDEX_NAME, index_schema=INDEX_SCHEMA, redis_url=REDIS_URL)
    redis_store.add_documents(documents)

def process_directory(directory_path):
    for file_path in glob.glob(os.path.join(directory_path, '*.json')):
        process_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rag_redis_process.py <path to JSON file or directory>")
        sys.exit(1)

    input_path = sys.argv[1]
    if os.path.isfile(input_path):
        process_file(input_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    else:
        print("Invalid path. Please provide a valid JSON file or directory path.")
        sys.exit(1)