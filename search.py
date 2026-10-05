from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import db

# Load the model once when the module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(texts):
    """Generate and return a numpy array of embeddings for a list of texts."""
    return model.encode(texts)

def build_index():
    """Read all entries, embed them, and build a FAISS index."""
    rows = db.get_all_entries()
    
    if not rows:
        return None, []
        
    texts = []
    for row in rows:
        # Safely parse triggers
        try:
            triggers = ", ".join(json.loads(row['triggers']))
        except Exception:
            triggers = ""
            
        # Combine situation and triggers
        text = f"{row['situation']} {triggers}"
        texts.append(text)
        
    # Get embeddings
    embeddings = get_embeddings(texts)
    
    # Convert to float32 (required by FAISS)
    embeddings = np.array(embeddings).astype('float32')
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Create Inner Product (IP) index which equals cosine similarity when normalized
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    
    # Add embeddings to the index
    index.add(embeddings)
    
    return index, rows

def find_similar(index, rows, query_text, current_id, k=3, threshold=0.55):
    """Find similar past entries, excluding the current one."""
    if index is None or index.ntotal == 0:
        return []
        
    # Embed the query text
    query_embedding = get_embeddings([query_text])
    query_embedding = np.array(query_embedding).astype('float32')
    
    # Normalize query for cosine similarity
    faiss.normalize_L2(query_embedding)
    
    # Search for top k matches (plus 1 in case it finds the exact same entry)
    distances, indices = index.search(query_embedding, k + 1)
    
    matches = []
    
    for i, idx in enumerate(indices[0]):
        dist = distances[0][i]
        matched_row = rows[idx]
        
        # Exclude the current entry by matching ID
        if matched_row['id'] == current_id:
            continue
            
        # For Inner Product on normalized vectors, higher score = more similar (max 1.0)
        if dist >= threshold:
            # Format the output dict
            try:
                emotions = ", ".join(json.loads(matched_row['emotions']))
            except Exception:
                emotions = "unknown"
                
            matches.append({
                "id": matched_row['id'],
                "created_at": matched_row['created_at'],
                "date": matched_row['created_at'][:10],
                "event": matched_row['event'],
                "emotions": emotions,
                "intensity": matched_row['intensity'],
                "raw": matched_row['raw']
            })
            
            # Stop if we have k valid matches
            if len(matches) == k:
                break
                
    return matches
