# rag_skrolli_json_process.py

import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from rag_redis.config import EMBED_MODEL, INDEX_NAME, REDIS_URL

def ingest_json_documents(json_directory):
    """
    Ingest JSON data to Redis, ensuring compatibility with the Redis index schema.
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

                all_texts = []
                all_metadatas = []

                for page in data['pages']:
                    page_content = page['content']
                    chunks = text_splitter.split_text(page_content)

                    for i, chunk in enumerate(chunks):
                        metadata = {
                            "issue": issue,
                            "source": f"Skrolli-lehti {issue}, sivu {page['page']}",
                            "start_index": i,
                            "content": chunk
                        }
                        all_metadatas.append(metadata)
                        all_texts.append(chunk)

                print(f"Done preprocessing {json_file}. Created {len(all_texts)} chunks.")

                _ = Redis.from_texts(
                    texts=all_texts,
                    metadatas=all_metadatas,
                    embedding=embedder,
                    index_name=INDEX_NAME,
                    index_schema = {
                    "text": [
                        {"name": "issue"},
                        {"name": "source"},
                        {"name": "content"},
                    ],
                    "numeric": [
                        {"name": "start_index"},
                    ],
                    "tag": [],
                },
                    redis_url=REDIS_URL,
                )

if __name__ == "__main__":
    json_directory = './json/'  # Adjust the path to your JSON directory
    ingest_json_documents(json_directory)