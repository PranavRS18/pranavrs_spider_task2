from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

from .rag_config import config_model
from .rag_parser import parse_documents

# Initialise the Model
vector_store_path = "./model_utils/chroma_langchain_db"
model, vector_store = config_model(vector_store_path)

def index_documents(files):
    # Add to the Vector Store
    all_splits = parse_documents(vector_store, files)

    if all_splits:
        print(f"\n\nStarted Adding {len(all_splits)} Documents to Vector Store.")
        vector_store.add_documents(documents = all_splits)
        print(f"Total Documents added to Vector Store : {len(all_splits)}")
        return True
    else:
        return False

# URLs of Research Paper
urls = ["https://arxiv.org/pdf/1706.03762", "https://arxiv.org/pdf/1810.04805",
        "https://arxiv.org/pdf/2005.14165", "https://arxiv.org/pdf/2210.08901", "https://arxiv.org/pdf/2302.13971"]
index_documents(urls)

# Prompt
prompt = hub.pull("rlm/rag-prompt")

# Define State
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define Retrieval
def retrieve(state: State):
    retrieved_docs_with_scores = vector_store.similarity_search_with_score(state["question"], k = 8)

    for i, (doc, score) in enumerate(retrieved_docs_with_scores):
        print(f"\n--- First Document Match {i+1} ---")
        print(f"Score: {score:.4f}")
        print(f"Content Preview:\n{doc.page_content[:300]}...")

    retrieved_docs = [doc for doc, score in retrieved_docs_with_scores]
    return {"context": retrieved_docs}

# Define Generation
def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = model.invoke(messages)
    return {"answer": response.content}


# Compile Application
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()