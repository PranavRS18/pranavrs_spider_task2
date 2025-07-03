import os

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

def config_model(persist_path):

    # Initiating the Chat Model and Embeddings Model
    model = init_chat_model("gemini-2.5-flash", model_provider = "google_genai")
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    print("Model has been initialised")

    # Chroma Vector Store
    vector_store = Chroma(
        collection_name = "rag_docs",
        embedding_function = embeddings,
        persist_directory = persist_path,
    )
    print("Vector Store has been initialised\n\n")
    return model, vector_store