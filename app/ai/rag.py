"""Retrieval-Augmented Generation (RAG) Engine."""
from typing import List, Tuple, Optional


class RAGEngine:
    """Implement RAG pattern for question answering."""

    def __init__(self, ai_service, vector_db):
        """Initialize RAG engine."""
        self.ai_service = ai_service
        self.vector_db = vector_db

    def retrieve_context(self, query: str, index: any, texts: List[str], k: int = 5) -> List[str]:
        """Retrieve relevant context for query."""
        # Create embedding for query
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(query)

        # Search in vector database
        distances, indices = self.vector_db.search(index, query_embedding, k)

        # Retrieve relevant texts
        relevant_texts = [texts[idx] for idx in indices if idx < len(texts)]
        return relevant_texts

    def generate_answer(self, query: str, context: List[str], sources: List[str] = None) -> dict:
        """Generate answer using context."""
        context_str = "\n\n".join(context)
        prompt = f"""Based on the following context, answer the question:

Context:
{context_str}

Question: {query}

Provide a clear and accurate answer based solely on the context provided."""

        answer = self.ai_service.generate_response(prompt)

        return {
            "answer": answer,
            "sources": sources or [],
            "context_used": len(context),
        }
