import os
import json
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
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
# LOAD EMBEDDINGS
# ============================================================

def load_embeddings():

    with open(
        EMBEDDINGS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    similarity = np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )

    return similarity


# ============================================================
# CREATE QUERY EMBEDDING
# ============================================================

def create_query_embedding(query):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    return response.embeddings[0].values


# ============================================================
# RETRIEVE TOP K CHUNKS
# ============================================================

def retrieve(query, top_k=3):

    embedded_chunks = load_embeddings()

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
# MAIN
# ============================================================

def main():

    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"Embeddings file not found:\n{EMBEDDINGS_PATH}"
        )

    query = input(
        "\nEnter your question: "
    )

    results = retrieve(
        query,
        top_k=3
    )

    print("\n================================")
    print("RETRIEVED CHUNKS")
    print("================================")

    for rank, result in enumerate(
        results,
        start=1
    ):

        print()
        print(
            f"--- RESULT {rank} ---"
        )

        print(
            f"Chunk ID: {result['id']}"
        )

        print(
            f"Similarity: {result['similarity']:.4f}"
        )

        print()

        print(result["text"])


if __name__ == "__main__":
    main()