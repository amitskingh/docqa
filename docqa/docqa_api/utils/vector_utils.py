import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def chunk_text(text: str, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


print(chunk_text(f"I'm great you know that right?"))


def create_vector_store(chunks):
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index, embeddings, chunks


def search_similar_chunks(index, chunks, question, top_k=3):
    q_emb = embedder.encode([question])
    D, I = index.search(q_emb, top_k)
    return [chunks[i] for i in I[0]]
