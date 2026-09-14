from pathlib import Path
import unicodedata
import re
import pdfplumber


# ============================================================
# Project paths
# ============================================================

PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

DATA_DIR = PROJECT_DIR / "data"

PDF_PATH = DATA_DIR / "arabic_document.pdf"
OUTPUT_PATH = DATA_DIR / "cleaned_arabic.txt"


# Create the data folder automatically
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Arabic helpers
# ============================================================

def contains_arabic(text):
    return bool(re.search(r"[\u0600-\u06FF]", text))


def normalize_token(token):
    token = unicodedata.normalize("NFKC", token)

    if contains_arabic(token):
        token = token[::-1]

    return token


def clean_line(line):
    if not line:
        return ""

    line = re.sub(r"\s+", " ", line).strip()

    if not line:
        return ""

    tokens = line.split()

    cleaned_tokens = [
        normalize_token(token)
        for token in tokens
    ]

    # Reverse word order for this specific PDF
    cleaned_tokens.reverse()

    return " ".join(cleaned_tokens)


# ============================================================
# Main extraction
# ============================================================

def extract_and_save():

    if not PDF_PATH.exists():
        raise FileNotFoundError(
            f"PDF not found:\n{PDF_PATH}"
        )

    all_pages = []

    with pdfplumber.open(PDF_PATH) as pdf:

        print(f"PDF: {PDF_PATH}")
        print(f"Pages: {len(pdf.pages)}")
        print()

        for page_number, page in enumerate(
            pdf.pages,
            start=1
        ):

            raw_text = page.extract_text()

            if not raw_text:
                print(
                    f"Page {page_number}: No text found"
                )
                continue

            cleaned_lines = []

            for line in raw_text.splitlines():

                cleaned = clean_line(line)

                if cleaned:
                    cleaned_lines.append(cleaned)

            page_text = "\n".join(cleaned_lines)

            all_pages.append(page_text)

            print(
                f"Processed page {page_number}"
            )

    final_text = "\n\n".join(all_pages)


    # ========================================================
    # CREATE / OVERWRITE OUTPUT FILE
    # ========================================================

    OUTPUT_PATH.write_text(
        final_text,
        encoding="utf-8"
    )
    # Verify that the file was actually written
    saved_text = OUTPUT_PATH.read_text(encoding="utf-8")
    
    print()
    print("========== FILE VERIFICATION ==========")
    print("Path:", OUTPUT_PATH)
    print("Characters in memory:", len(final_text))
    print("Characters in file:", len(saved_text))
    print("First 500 characters from file:")
    print(saved_text[:500])
    print("=======================================")

    # ========================================================
    # Confirmation
    # ========================================================

    print()
    print("================================")
    print("DONE")
    print("================================")

    print(f"File created/updated:")
    print(OUTPUT_PATH)

    print(f"Characters: {len(final_text)}")
    print(f"Exists: {OUTPUT_PATH.exists()}")
    print(f"Size: {OUTPUT_PATH.stat().st_size} bytes")

    print()
    print("First 1000 characters:")
    print("--------------------------------")

    print(final_text[:1000])


if __name__ == "__main__":
    extract_and_save()