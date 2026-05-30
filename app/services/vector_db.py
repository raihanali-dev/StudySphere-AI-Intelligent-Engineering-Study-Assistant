"""Vector database service."""
from typing import List, Tuple
import json


class VectorDB:
    """Handle vector database operations."""

    def __init__(self, db_path: str = "vector_db"):
        """Initialize vector database."""
        self.db_path = db_path
        try:
            import faiss
            self.faiss = faiss
        except ImportError:
            raise ImportError("FAISS is required. Install with: pip install faiss-cpu")

    def create_embeddings(self, texts: List[str]) -> Tuple[List[List[float]], any]:
        """Create embeddings for texts using Sentence Transformers."""
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(texts)
        return embeddings, model

    def add_to_index(self, embeddings: List[List[float]], metadata: List[dict] = None):
        """Add embeddings to FAISS index."""
        import numpy as np

        embeddings_array = np.array(embeddings).astype("float32")
        index = self.faiss.IndexFlatL2(embeddings_array.shape[1])
        index.add(embeddings_array)

        return index

    def search(self, index: any, query_embedding: List[float], k: int = 5) -> Tuple[List[float], List[int]]:
        """Search for similar embeddings."""
        import numpy as np

        query_array = np.array([query_embedding]).astype("float32")
        distances, indices = index.search(query_array, k)
        return distances[0], indices[0]
