from pathlib import Path
import re
import unicodedata


# ============================================================
# Paths
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

INPUT_PATH = PROJECT_DIR / "data" / "cleaned_arabic.txt"
OUTPUT_PATH = PROJECT_DIR / "data" / "final_text.txt"


# ============================================================
# Cleaning function
# ============================================================

def clean_text(text: str) -> str:

    # Normalize Unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Normalize spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )

    # Remove spaces before punctuation
    text = re.sub(
        r"\s+([،؛:.)])",
        r"\1",
        text
    )

    # Remove spaces after opening brackets
    text = re.sub(
        r"([(\[])\s+",
        r"\1",
        text
    )

    return text.strip()


# ============================================================
# Main
# ============================================================

def main():

    # Check input file
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found:\n{INPUT_PATH}"
        )

    # Read cleaned Arabic text
    text = INPUT_PATH.read_text(
        encoding="utf-8"
    )

    # Clean text
    cleaned = clean_text(text)

    # Save final text
    OUTPUT_PATH.write_text(
        cleaned,
        encoding="utf-8"
    )

    # Show results
    print("Cleaning complete.")
    print()
    print(f"Input file:")
    print(INPUT_PATH)

    print()
    print(f"Output file:")
    print(OUTPUT_PATH)

    print()
    print(f"Characters before: {len(text)}")
    print(f"Characters after:  {len(cleaned)}")

    print()
    print("File exists:", OUTPUT_PATH.exists())
    print(
        "File size:",
        OUTPUT_PATH.stat().st_size,
        "bytes"
    )

    print()
    print("First 1000 characters:")
    print("--------------------------------")
    print(cleaned[:1000])


if __name__ == "__main__":
    main()