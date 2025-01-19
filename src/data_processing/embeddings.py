import os
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm  # For a better progress bar

# Paths
INPUT_DIR = r'data/processed/chunks'  # Path to the chunked text files
OUTPUT_DIR = r'data/processed/embeddings'  # Where embeddings will be saved

# Create the embeddings directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the pre-trained model (you can choose any compatible model here)
MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

def generate_embeddings_in_batches(text_chunks, batch_size=32):
    """
    Generate embeddings for text chunks in batches.
    Args:
        text_chunks (list): List of text chunks.
        batch_size (int): Number of chunks to process in each batch.
    Returns:
        numpy.ndarray: Array of embeddings.
    """
    embeddings = []
    for i in tqdm(range(0, len(text_chunks), batch_size), desc="Generating embeddings"):
        batch = text_chunks[i:i + batch_size]
        embeddings.extend(model.encode(batch, show_progress_bar=False))
    return embeddings

def process_chunks_and_generate_embeddings(input_dir, output_dir):
    """
    Process chunked text files and generate embeddings, saving them as pickle files.
    Args:
        input_dir (str): Path to the directory containing chunked text files.
        output_dir (str): Path to the directory to save embeddings.
    Returns:
        dict: A dictionary mapping filenames to their generated embeddings.
    """
    embeddings = {}
    
    # Process all text chunk files
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_dir, filename)
            
            try:
                # Read the chunked text file
                with open(input_file, 'r', encoding='utf-8') as f:
                    chunks = [line.strip() for line in f if line.strip()]
                
                # Skip empty files
                if not chunks:
                    print(f"Warning: {filename} is empty. Skipping this file.")
                    continue
                
                # Generate embeddings in batches
                chunk_embeddings = generate_embeddings_in_batches(chunks)
                
                # Save the embeddings to a compressed pickle file
                embedding_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_embeddings.pkl")
                with open(embedding_file, 'wb') as f_out:
                    pickle.dump(chunk_embeddings, f_out, protocol=pickle.HIGHEST_PROTOCOL)
                
                embeddings[filename] = chunk_embeddings
                print(f"Embeddings for {filename} successfully saved to {embedding_file}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return embeddings

if __name__ == "__main__":
    print(f"Using SentenceTransformer model: {MODEL_NAME}")
    print(f"Input Directory: {INPUT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    
    # Run the embedding generation process
    all_embeddings = process_chunks_and_generate_embeddings(INPUT_DIR, OUTPUT_DIR)
    print(f"Embedding generation complete. Total files processed: {len(all_embeddings)}")
