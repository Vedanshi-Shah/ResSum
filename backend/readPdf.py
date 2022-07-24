import pdfplumber
with pdfplumber.open(r'temp.pdf') as pdf:
    first_page = pdf.pages[1]
    print(first_page.extract_text())