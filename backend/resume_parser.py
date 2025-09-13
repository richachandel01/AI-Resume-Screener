import spacy
import pdfplumber
import docx2txt

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def parse_resume(text):
    doc = nlp(text)
    return {
        "emails": [ent.text for ent in doc.ents if ent.label_ == "EMAIL"],
        "names": [ent.text for ent in doc.ents if ent.label_ == "PERSON"],
        "skills": [],  # skills ko baad me custom logic se fill karenge
    }


# test ke liye
if __name__ == "__main__":
    sample_pdf = "C:/Users/chand/OneDrive/Desktop/RichaChandel_RESUME.pdf"
    text = extract_text_from_pdf(sample_pdf)
    parsed = parse_resume(text)
    print(parsed)
