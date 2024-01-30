from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from rag_redis.config import (
    EMBED_MODEL,
    INDEX_NAME,
    INDEX_SCHEMA,
    REDIS_URL,
)


# Make this look better in the docs.
class Question(BaseModel):
    __root__: str


# Init Embeddings
embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

# Connect to pre-loaded vectorstore
# run the ingest.py script to populate this
vectorstore = Redis.from_existing_index(
    embedding=embedder, index_name=INDEX_NAME, schema=INDEX_SCHEMA, redis_url=REDIS_URL
)
# TODO allow user to change parameters
retriever = vectorstore.as_retriever(search_type="mmr")


# Define our prompt
template = """
Tämä on Skrolli-lehteen liittyvän tietouden tietokantahaku. Koita olla mahdollisimman kattava vastauksessasi.

Konteksti:
---------
{context}

---------
Kysymys: {question}
---------

Answer:
"""


prompt = ChatPromptTemplate.from_template(template)


# RAG Chain
model = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
).with_types(input_type=Question)