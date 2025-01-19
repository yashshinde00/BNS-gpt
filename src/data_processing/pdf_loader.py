import os
from PyPDF2 import PdfReader

# Define the paths
input_dir = r'data/raw'  # Path to raw PDFs
output_dir = r'data/processed/cleaned'  # Path to cleaned text files

# Ensure the processed directory exists
os.makedirs(output_dir, exist_ok=True)

def load_pdfs(input_dir, output_dir):
    """
    Extract text from each PDF in the raw data folder and save it as a text file in the processed folder.
    """
    # Get all PDF files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processing {pdf_path}...")

            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_path)
            
            # Save the extracted text to a .txt file in the processed directory
            output_file = os.path.join(output_dir, f'{filename}.txt')
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(extracted_text)
            
            print(f"Text from {filename} saved to {output_file}")

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using PyPDF2.
    """
    reader = PdfReader(pdf_path)
    extracted_text = ""
    
    # Extract text from each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        extracted_text += page.extract_text()
    
    return extracted_text

# Run the PDF loader
load_pdfs(input_dir, output_dir)
