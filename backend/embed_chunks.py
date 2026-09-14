import os
import re
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

CHUNKS_PATH = PROJECT_DIR / "data" / "chunks.txt"
OUTPUT_PATH = PROJECT_DIR / "data" / "embeddings.json"


# ============================================================
# GEMINI SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)


# ============================================================
# READ CHUNKS
# ============================================================

def load_chunks():

    text = CHUNKS_PATH.read_text(
        encoding="utf-8"
    )

    pattern = r"===== CHUNK (\d+) =====\n(.*?)(?=\n===== CHUNK \d+ =====|\Z)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )

    chunks = []

    for chunk_number, chunk_text in matches:

        chunks.append({
            "id": int(chunk_number),
            "text": chunk_text.strip()
        })

    return chunks


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks):

    embedded_chunks = []

    for i, chunk in enumerate(chunks, start=1):

        print(f"Embedding chunk {i}/{len(chunks)}...")

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk["text"]
        )

        embedding = response.embeddings[0].values

        embedded_chunks.append({
            "id": chunk["id"],
            "text": chunk["text"],
            "embedding": embedding
        })

    return embedded_chunks


# ============================================================
# MAIN
# ============================================================

def main():

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunks file not found:\n{CHUNKS_PATH}"
        )

    chunks = load_chunks()

    print("Chunks loaded:", len(chunks))
    print()

    embedded_chunks = create_embeddings(chunks)

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embedded_chunks,
            file,
            ensure_ascii=False
        )

    print()
    print("================================")
    print("Embedding complete.")
    print("================================")
    print(f"Total chunks: {len(embedded_chunks)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()