# rag_qa_json_process.py

import json
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from rag_redis.config import EMBED_MODEL, INDEX_NAME, REDIS_URL

def ingest_qa_json_documents(json_directory):
    """
    Ingest Q&A JSON data to Redis, ensuring compatibility with the Redis index schema.
    """
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    for json_file in os.listdir(json_directory):
        if json_file.endswith('.json'):
            with open(os.path.join(json_directory, json_file), 'r') as file:
                qa_data = json.load(file)

                all_texts = []
                all_metadatas = []

                for qa_pair in qa_data:
                    qa_text = f"Q: {qa_pair['question']} A: {qa_pair['answer']}"
                    metadata = {
                        "question": qa_pair['question'],
                        "answer": qa_pair['answer'],
                        "references": qa_pair.get('references', '')
                    }
                    all_metadatas.append(metadata)
                    all_texts.append(qa_text)

                print(f"Done preprocessing {json_file}. Created {len(all_texts)} Q&A pairs.")

                _ = Redis.from_texts(
                    texts=all_texts,
                    metadatas=all_metadatas,
                    embedding=embedder,
                    index_name=INDEX_NAME,
                    index_schema = {
                        "text": [
                            {"name": "question"},
                            {"name": "answer"},
                            {"name": "references"},
                        ],
                        "tag": [],
                    },
                    redis_url=REDIS_URL,
                )

if __name__ == "__main__":
    json_directory = './qa_json/'  # Adjust the path to your Q&A JSON directory
    ingest_qa_json_documents(json_directory)