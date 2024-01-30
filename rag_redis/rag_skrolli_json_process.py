# rag_skrolli_json_process.py

import json
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from rag_redis.config import EMBED_MODEL, INDEX_NAME, INDEX_SCHEMA, REDIS_URL
# from rag_redis.config import EMBED_MODEL, INDEX_NAME, REDIS_URL

""" INDEX_SCHEMA = {
    'text': [{'name': 'issue'}],
    'numeric': [{'name': 'page'}, {'name': 'chunk_index'}],
    'vector': [{'name': 'content_vector', 'algorithm': 'HNSW', 'datatype': 'FLOAT32', 'dims': 384, 'distance_metric': 'COSINE'}]
}
 """

print(f"Index schema: {INDEX_SCHEMA}")

def ingest_json_documents(json_directory):
    """
    Ingest JSON data to Redis.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=100, length_function=len, is_separator_regex=False
    )
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    for json_file in os.listdir(json_directory):
        if json_file.endswith('.json'):
            with open(os.path.join(json_directory, json_file), 'r') as file:
                data = json.load(file)
                issue = data['issue']

                # Generate metadata
                metadatas = [{"issue": issue, "page": page['page'], "chunk_index": i} for page in data['pages'] for i, _ in enumerate(text_splitter.split_text(page['content']))]

                # Print some sample metadata for debugging
                print("Sample metadata:", metadatas[:3])  # Print first 3 metadata entries for inspection

                all_chunks = []
                for page in data['pages']:
                    chunks = text_splitter.split_text(page['content'])  # Correct method call
                    all_chunks.extend(chunks)

                print(f"Done preprocessing {json_file}. Created {len(all_chunks)} chunks.")

                _ = Redis.from_texts(
                    texts=[f"Skrolli magazine issue: {issue}. Page {page['page']}: " + chunk for page in data['pages'] for chunk in text_splitter.split_text(page['content'])],  # Updated line
                    metadatas=[{"issue": issue, "page": page['page'], "chunk_index": i} for page in data['pages'] for i, _ in enumerate(text_splitter.split_text(page['content']))],  # Updated line
                    embedding=embedder,
                    index_name=INDEX_NAME,
                    index_schema=INDEX_SCHEMA,
                    redis_url=REDIS_URL,
                )

if __name__ == "__main__":
    json_directory = './json/'
    ingest_json_documents(json_directory)