import os
import pickle
import faiss
import numpy as np

# Paths
EMBEDDING_DIR = r'data/processed/embeddings'
INDEX_FILE = r'data/processed/faiss_index/index.faiss'
ID_FILE = r'data/processed/faiss_index/doc_ids.pkl'

os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

def load_embeddings(embedding_dir):
    """
    Load all embeddings and their associated document IDs.
    Args:
        embedding_dir (str): Directory containing embeddings as pickle files.
    Returns:
        tuple: A list of embeddings and a list of document IDs.
    """
    embeddings = []
    doc_ids = []
    for filename in os.listdir(embedding_dir):
        if filename.endswith('_embeddings.pkl'):
            file_path = os.path.join(embedding_dir, filename)
            with open(file_path, 'rb') as f:
                file_embeddings = pickle.load(f)
                embeddings.extend(file_embeddings)
                doc_ids.extend([filename] * len(file_embeddings))
    return np.array(embeddings), doc_ids

def create_faiss_index(embedding_dir, index_file, id_file):
    """
    Create a FAISS index from embeddings and save it.
    Args:
        embedding_dir (str): Directory containing embeddings.
        index_file (str): Path to save the FAISS index.
        id_file (str): Path to save document IDs.
    """
    embeddings, doc_ids = load_embeddings(embedding_dir)
    
    if len(embeddings) == 0:
        raise ValueError("No embeddings found. Ensure the embedding directory is populated.")

    # Create a FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)  # L2 distance for similarity
    index.add(embeddings)
    
    # Save the index and document IDs
    faiss.write_index(index, index_file)
    with open(id_file, 'wb') as f:
        pickle.dump(doc_ids, f)
    
    print(f"FAISS index created and saved to {index_file}")
    print(f"Document IDs saved to {id_file}")

def load_faiss_index(index_file, id_file):
    """
    Load a FAISS index and its associated document IDs.
    Args:
        index_file (str): Path to the FAISS index file.
        id_file (str): Path to the document IDs file.
    Returns:
        tuple: A FAISS index and a list of document IDs.
    """
    index = faiss.read_index(index_file)
    with open(id_file, 'rb') as f:
        doc_ids = pickle.load(f)
    return index, doc_ids

if __name__ == "__main__":
    create_faiss_index(EMBEDDING_DIR, INDEX_FILE, ID_FILE)
