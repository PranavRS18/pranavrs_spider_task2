import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model_utils.rag_init import index_documents, graph

app = FastAPI()

origins = [
    os.getenv("CLIENT_URL"),
    os.getenv("CLIENT_URL").replace("localhost", "127.0.0.1"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/api/v1/")
def read_root():
    return {"message": "Welcome to AskMyPaper RAG API!"}

@app.post("/api/v1/ask")
def ask_question(payload: QuestionRequest):
    response = graph.invoke({"question": payload.question})
    return {
        "question": payload.question,
        "answer": response["answer"]
    }

@app.post("/api/v1/analysis")
def analyse_link(payload: QuestionRequest):
    response = index_documents([payload.question])
    return {
        "success": response,
    }
