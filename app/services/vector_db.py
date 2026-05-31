"""Vector database service using Chromadb (lightweight for Railway)."""
from typing import List, Tuple, Optional
import json


class VectorDB:
    """Handle vector database operations using Chromadb."""

    def __init__(self, db_path: str = "vector_db"):
        """Initialize vector database with Chromadb."""
        import chromadb
        
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = None

    def create_collection(self, collection_name: str = "study_materials") -> None:
        """Create or get a Chromadb collection."""
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_to_index(self, texts: List[str], metadata: List[dict] = None, ids: List[str] = None) -> None:
        """Add texts to Chromadb collection with automatic embeddings."""
        if self.collection is None:
            self.create_collection()
        
        # Chromadb automatically embeds using all-MiniLM-L6-v2
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        
        if metadata is None:
            metadata = [{"source": "study_material"} for _ in texts]
        
        self.collection.add(
            documents=texts,
            metadatas=metadata,
            ids=ids
        )

    def search(self, query: str, k: int = 5) -> Tuple[List[str], List[float]]:
        """Search for similar documents using query text."""
        if self.collection is None:
            raise RuntimeError("Collection not initialized. Call create_collection first.")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        # Extract documents and distances
        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        return documents, distances

    def delete_collection(self, collection_name: str) -> None:
        """Delete a collection."""
        self.client.delete_collection(name=collection_name)
        self.collection = None
