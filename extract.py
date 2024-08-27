import pymupdf
from glob import glob
import os

def format_txtpath_from_pdfpath(pdf_path):
    pdf_file = pdf_path.split('/')[-1]
    base_name = pdf_file.split('.')[0]
    return os.path.join('extractions', base_name + ".txt")

def save_text_to_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content) 

def extract_pdfs(pdf):
    doc = pymupdf.open(pdf)
    return "\n\n\n".join([page.get_text() for page in doc])

def main():
    files = glob('pdfs/*pdf')
    for pdf in files:
        content = extract_pdfs(pdf)
        print(f"Extracted content from {pdf}")
        file_name = format_txtpath_from_pdfpath(pdf)
        save_text_to_file(file_name, content)
        print(f"Saved content to {file_name}")


if __name__ == "__main__":
    main()