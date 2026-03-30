import sys
from pypdf import PdfReader

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    pdf_file = "/Users/yogiphil/Desktop/WEB DEVELOPMENT PROJECT/EXAMPLE1/pages/Nghi quy Chua Lanh Benh Tat.pdf"
    print(extract_text(pdf_file))
