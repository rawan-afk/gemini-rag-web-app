from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

INPUT_PATH = PROJECT_DIR / "data" / "final_text.txt"
OUTPUT_PATH = PROJECT_DIR / "data" / "chunks.txt"


# ============================================================
# CHUNKING
# ============================================================

def create_chunks(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        # Try to stop at a paragraph/newline
        if end < text_length:

            newline_position = text.rfind(
                "\n",
                start,
                end
            )

            if newline_position > start:
                end = newline_position

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Move forward while keeping overlap
        next_start = end - overlap

        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


# ============================================================
# MAIN
# ============================================================

def main():

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_PATH}"
        )

    text = INPUT_PATH.read_text(
        encoding="utf-8"
    )

    chunks = create_chunks(text)

    print("Chunking complete.")
    print()
    print(f"Total characters: {len(text)}")
    print(f"Total chunks: {len(chunks)}")

    print()
    print("================================")
    print("FIRST 5 CHUNKS")
    print("================================")

    for i, chunk in enumerate(
        chunks[:5],
        start=1
    ):

        print()
        print(f"--- CHUNK {i} ---")
        print(chunk)
        print()
        print(f"Characters: {len(chunk)}")

    # Save chunks
    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        for i, chunk in enumerate(
            chunks,
            start=1
        ):

            file.write(
                f"\n===== CHUNK {i} =====\n"
            )

            file.write(chunk)

            file.write("\n")


if __name__ == "__main__":
    main()