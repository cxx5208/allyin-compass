import fitz  # PyMuPDF
import email
import os
import json
import glob
import sys

# Add the parent directory to the Python path to import security module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from security.pii_filter import find_pii # Import find_pii
from security.compliance_tagger import tag_compliance # Import tag_compliance

def parse_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
        text = None
    return text

def parse_eml(eml_path):
    """Extracts subject and body from an EML file."""
    subject = None
    body = None
    try:
        with open(eml_path, 'r', encoding='utf-8', errors='ignore') as f:
            msg = email.message_from_file(f)
            subject = msg['subject']

            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = part.get('Content-Disposition')

                    # Look for plain text parts
                    if ctype == 'text/plain' and cdispo is None:
                        body = part.get_payload(decode=True).decode()
                        break # Get the first plain text part
            else:
                body = msg.get_payload(decode=True).decode()

    except Exception as e:
        print(f"Error parsing EML {eml_path}: {e}")
        subject = None
        body = None

    return subject, body

def process_unstructured_data(data_dir='data/unstructured', output_jsonl='data/unstructured/parsed.jsonl'):
    """Processes unstructured data files (PDF and EML) and saves as JSONL."""
    os.makedirs(data_dir, exist_ok=True)

    # Get list of PDF and EML files
    pdf_files = glob.glob(os.path.join(data_dir, '*.pdf'))
    eml_files = glob.glob(os.path.join(data_dir, '*.eml'))

    all_files = pdf_files + eml_files

    if not all_files:
        print(f"No PDF or EML files found in {data_dir}")
        return

    with open(output_jsonl, 'w', encoding='utf-8') as outfile:
        for file_path in all_files:
            doc_data = {
                'filepath': file_path,
                'filename': os.path.basename(file_path),
                'text': None,
                'subject': None,
                'pii_tags': {},
                'compliance_tags': []
            }
            extracted_text = None

            if file_path.endswith('.pdf'):
                extracted_text = parse_pdf(file_path)
            elif file_path.endswith('.eml'):
                subject, body = parse_eml(file_path)
                doc_data['subject'] = subject
                extracted_text = body # Store email body here for PII/compliance check

            doc_data['text'] = extracted_text # Store the extracted text (or None)

            # Find PII and compliance tags if text was extracted
            if extracted_text:
                doc_data['pii_tags'] = find_pii(extracted_text)
                doc_data['compliance_tags'] = tag_compliance(extracted_text)

            # Only write to JSONL if there's some content or metadata
            if doc_data['text'] is not None or doc_data['subject'] is not None or doc_data['pii_tags'] or doc_data['compliance_tags']:
                json.dump(doc_data, outfile)
                outfile.write('\n')
                print(f"Processed {file_path} - PII: {doc_data['pii_tags']}, Compliance: {doc_data['compliance_tags']}")
            else:
                print(f"Skipping {file_path} due to parsing errors or no content.")

if __name__ == "__main__":
    process_unstructured_data() 