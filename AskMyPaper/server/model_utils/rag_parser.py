import os
import requests
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create Directory if not exists
os.makedirs("./papers", exist_ok = True)

def parse_documents(vector_store, files):
    docs = []
    existing_docs = [meta["source"] for meta in vector_store.get()["metadatas"]]

    # Download the Research Papers
    for i in range(len(files)):
        filename = f"./papers/research_paper_{files[i].replace("https://", "").replace("/", "_")}.pdf"
        if filename in existing_docs: print(f"File {i + 1} ({files[i]}) has already been parsed and added to the vector store.")
        else:
            try:
                response = requests.get(files[i], timeout = 15)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to download {files[i]}: {e}")
                continue

            print(f"Parsing File {i + 1} ({files[i]})")
            with open(filename, "wb") as f:
                f.write(response.content)

            try:
                # Load the PDF
                loader = PyPDFLoader(filename)
                doc = loader.load()
                docs.extend(doc)
                print(f"File {i + 1} ({files[i]}) -> Documents Found : {len(docs)}\n")
            except Exception as e:
                print(f"Failed to parse {files[i]}: {e}")
                continue

    # Split the Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    all_splits = text_splitter.split_documents(docs)

    for i, doc in enumerate(all_splits[:5]):
        print(f"\n--- Chunk Preview #{i+1} ---")
        print(f"{doc.page_content[:300]}...")

    return all_splits