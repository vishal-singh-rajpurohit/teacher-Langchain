from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface.embeddings import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()

embedding_model = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

vector_store = Chroma(
    persist_directory="./chroma_db/chroma_db",
    embedding_function=embedding_model
)

