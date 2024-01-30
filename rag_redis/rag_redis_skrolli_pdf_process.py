# rag_redis_skrolli_pdf_process.py
# for langchain + rag

import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from rag_redis.config import EMBED_MODEL, INDEX_NAME, INDEX_SCHEMA, REDIS_URL

def ingest_documents(data_directory):
    """
    Ingest PDFs to Redis from the specified data directory.
    """
    # Load list of pdfs
    pdf_files = [file for file in os.listdir(data_directory) if file.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified directory:", data_directory)
        return

    print("Found PDF files:", pdf_files)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=100, add_start_index=True
    )

    for pdf_file in pdf_files:
        doc_path = os.path.join(data_directory, pdf_file)

        print("Parsing PDF file:", doc_path)

        loader = UnstructuredFileLoader(doc_path, mode="single", strategy="fast")
        chunks = loader.load_and_split(text_splitter)

        print("Done preprocessing. Created", len(chunks), "chunks of the PDF")

        # Create vectorstore for each PDF
        embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

        _ = Redis.from_texts(
            # You can customize metadata as needed
            texts=[f"PDF: Skrolli-lehti {pdf_file.split('-')[0]}.{pdf_file.split('-')[1][0]}. " + chunk.page_content for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
            embedding=embedder,
            index_name=INDEX_NAME,
            index_schema=INDEX_SCHEMA,
            redis_url=REDIS_URL,
        )

if __name__ == "__main__":
    data_directory = "./data/"  # Update with the path to your PDFs directory
    ingest_documents(data_directory)