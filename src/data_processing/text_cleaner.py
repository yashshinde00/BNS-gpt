import os
import re

# Define the paths
input_dir = r'data/processed/cleaned'  # Path to the extracted text files
output_dir = r'data/processed/cleaned'  # Where cleaned text will be saved

# Ensure the cleaned directory exists
os.makedirs(output_dir, exist_ok=True)

def clean_text(text):
    """
    Clean the extracted text by removing unwanted characters and formatting.
    """
    # Remove unnecessary whitespace, newlines, and special characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces or newlines with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove non-alphanumeric characters except spaces
    return text.strip()  # Remove leading and trailing spaces

def clean_text_files(input_dir, output_dir):
    """
    Clean all extracted text files in the processed folder.
    """
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            cleaned_text = clean_text(text)
            
            # Save cleaned text to a new file in the cleaned folder
            output_file = os.path.join(output_dir, filename)
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(cleaned_text)
            
            print(f"Cleaned text from {filename} saved to {output_file}")

# Run the cleaner
clean_text_files(input_dir, output_dir)
