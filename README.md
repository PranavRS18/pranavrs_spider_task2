# Spider ML Task 2
## AskMyPaper (Task 2 - A)

**AskMyPaper** is an AI-based web application that allows users to ask research papers in natural language. Supported scholarly PDFs can be uploaded by the user, and the application uses Retrieval-Augmented Generation (RAG) to return contextual answers directly from the paper content.

### Features

- **Upload and parse scholarly PDF files from credible sources**
- Automatically extracts and includes paper contents within a vector store
- **Ask questions and get context-aware replies**
  - Frontend typing-style animated responses
  - Vue 3 Composition API frontend
  - LangChain, Chroma, and Gemini/Google Generative AI-enabled FastAPI backend
  - Axios and CORS integration
  - Dark-themed responsive UI

### Frontend

- Composition API and Vue 3 based
- Simulated typing effect for answers
- Clean, minimal design using simple color variables

### Backend

- Built using **FastAPI** with proper CORS support
- Uses **LangChain** for chaining language model tasks
- Integrated with **Google Gemini 2.0 Flash**
- Supports PDF parsing, chunking, and embedding into Chroma DB vector store
- Async endpoints in **FastAPI** and **Axios-based** requests from the frontend
- Quota exhaustion and retry error handling

### RAG Pipeline

- **PDF file parsing** into chunks
- Chunks are injected with a vectorizer and placed within the **Chroma** vector store
- Upon user query, the most applicable chunks are fetched
- These chunks are fed into the **LLM** to provide a contextually aware answer

### Tech Stack

#### Frontend

- **Vue 3** using Composition API
- **Axios** for HTTP requests
- **Vite** as the build tool
- **HTML/CSS** with scoped styling and theme control variables

#### Backend

- **FastAPI** — fast async Python web framework for production
- **LangChain** — for orchestration and retrieval of LLMs
- **Chroma** — document embedding vector store
- **Google Gemini 2.0 Flash** — employed for providing answers
- **Uvicorn** — ASGI server for development

### Why Only Trusted Scholarly Domains?

To ensure reliability and quality, AskMyPaper permits PDF uploads only from very credible research repositories. This guarantees:

- **High Content Quality**: Reputable domains (e.g., arXiv.org) offer structured, peer-reviewed, or preprint scholarly content.
- **Format Consistency**: These domains employ conventional layouts that are simpler to parse and analyze efficiently.
- **Less Noise**: Prohibiting generic PDFs or PDFs behind intricate HTML layers (such as those from ieeexplore.ieee.org) prevents parsing mistakes and irrelevant content ingestion.
- **Scalable Validation**: Restricting accepted sources makes metadata validation and content extraction easier.

### Default 5 AskMyPaper's Research Papers:
- Attention Is All You Need
- BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- GPT-3: Language Models are Few-Shot Learners
- Contrastive Language-Image Pretraining with Knowledge Graphs
- LLaMA: Open and Efficient Foundation Language Models