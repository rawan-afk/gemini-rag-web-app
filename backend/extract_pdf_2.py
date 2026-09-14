import pdfplumber

pdf_path = "../data/arabic_document.pdf"

with pdfplumber.open(pdf_path) as pdf:

    print("Number of pages:", len(pdf.pages))

    page = pdf.pages[0]

    text = page.extract_text()

    print("\nEXTRACTED TEXT:\n")
    print(text[:2000])

    with open("../data/extracted_pdfplumber.txt", "w", encoding="utf-8") as f:
        f.write(text)