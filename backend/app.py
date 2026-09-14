import os
import json
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

EMBEDDINGS_PATH = PROJECT_DIR / "data" / "embeddings.json"


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST FORMAT
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# LOAD EMBEDDINGS
# ============================================================

with open(
    EMBEDDINGS_PATH,
    "r",
    encoding="utf-8"
) as file:

    embedded_chunks = json.load(file)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )


# ============================================================
# QUERY EMBEDDING
# ============================================================

def create_query_embedding(query):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    return response.embeddings[0].values


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(query, top_k=3):

    query_embedding = create_query_embedding(query)

    results = []

    for chunk in embedded_chunks:

        similarity = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        results.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "similarity": similarity
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]


# ============================================================
# RAG CHAT
# ============================================================

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    # Retrieve relevant chunks
    retrieved_chunks = retrieve(
        request.message,
        top_k=3
    )

    # Build context
    context = "\n\n".join(
        [
            f"[Chunk {chunk['id']}]\n{chunk['text']}"
            for chunk in retrieved_chunks
        ]
    )

    # Create RAG prompt
    prompt = f"""
You are an assistant answering questions based on the provided document.

Use the context below to answer the user's question.

Rules:
- Answer using the provided context.
- Do not invent information.
- If the answer is not available in the context, say that the information is not available in the document.
- Answer clearly and directly.
- The document is in Arabic, so answer in Arabic when the user asks in Arabic.

Context:
{context}

User Question:
{request.message}
"""

    # Generate answer
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return {
        "response": response.text
    }


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Gemini RAG API is running"
    }