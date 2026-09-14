import pymupdf

pdf_path = "../data/arabic_document.pdf"

doc = pymupdf.open(pdf_path)

print("Number of pages:", len(doc))

# Extract first page
page = doc[0]
text = page.get_text("text", sort=True)

# Save extracted text to a UTF-8 file
with open("../data/extracted.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Show Python's raw representation
print("\nRAW TEXT:")
print(repr(text[:500]))

doc.close()