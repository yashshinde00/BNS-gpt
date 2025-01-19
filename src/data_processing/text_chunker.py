import os

# Define the paths
input_dir = r'data/processed/cleaned'  # Path to cleaned text files
output_dir = r'data/processed/chunks'  # Where chunked text will be saved

# Ensure the chunks directory exists
os.makedirs(output_dir, exist_ok=True)

def chunk_text(text, chunk_size=1000):
    """
    Split the cleaned text into smaller chunks of specified size (characters).
    """
    # Split the text into chunks of the given size
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def chunk_text_files(input_dir, output_dir, chunk_size=1000):
    """
    Split all cleaned text files into chunks.
    """
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Split text into chunks
            chunks = chunk_text(text, chunk_size)
            
            # Save each chunk as a new file
            for idx, chunk in enumerate(chunks):
                chunk_filename = f"{filename}_chunk_{idx + 1}.txt"
                output_file = os.path.join(output_dir, chunk_filename)
                with open(output_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(chunk)
                
                print(f"Chunk {idx + 1} of {filename} saved to {output_file}")

# Run the chunker
chunk_text_files(input_dir, output_dir)
