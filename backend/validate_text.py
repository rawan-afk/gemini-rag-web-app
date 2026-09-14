from pathlib import Path
import re


PROJECT_DIR = Path(
    r"C:\Users\rawan\OneDrive\Desktop\gemini-web-app"
)

INPUT_PATH = PROJECT_DIR / "data" / "final_text.txt"


# Common PDF extraction problems
patterns = {
    "space_inside_word": r"\b[\u0600-\u06FF]+\s+[\u0600-\u06FF]+\b",
    "wrong_fi": r"ف\s+ى",
    "wrong_al": r"ا\s+ل",
}


def main():

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"File not found:\n{INPUT_PATH}"
        )

    text = INPUT_PATH.read_text(
        encoding="utf-8"
    )

    print("Validation report")
    print("=" * 50)

    # Check suspicious spaces inside Arabic words
    matches = re.findall(
        patterns["space_inside_word"],
        text
    )

    print(
        f"\nPossible split Arabic words: {len(matches)}"
    )

    for item in matches[:30]:
        print("-", item)

    # Check "في" extracted as "ف ى"
    fi_matches = re.findall(
        patterns["wrong_fi"],
        text
    )

    print(
        f"\nPossible 'ف ى' errors: {len(fi_matches)}"
    )

    # Check "ال" split
    al_matches = re.findall(
        patterns["wrong_al"],
        text
    )

    print(
        f"\nPossible 'ا ل' errors: {len(al_matches)}"
    )


if __name__ == "__main__":
    main()