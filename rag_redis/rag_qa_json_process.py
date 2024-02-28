# rag_qa_json_process.py

import json
import os
import argparse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from rag_redis.config import EMBED_MODEL, INDEX_NAME, REDIS_URL

def ingest_qa_json_document(file_path):
    embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    with open(file_path, 'r') as file:
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

        print(f"Done preprocessing {os.path.basename(file_path)}. Created {len(all_texts)} Q&A pairs.")

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

def process_path(path):
    if os.path.isdir(path):
        for json_file in os.listdir(path):
            if json_file.endswith('.json'):
                ingest_qa_json_document(os.path.join(path, json_file))
    elif os.path.isfile(path) and path.endswith('.json'):
        ingest_qa_json_document(path)
    else:
        print(f"Invalid path or file format: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a JSON file or a directory containing JSON files.")
    parser.add_argument("path", help="Path to the JSON file or directory")
    args = parser.parse_args()
    process_path(args.path)