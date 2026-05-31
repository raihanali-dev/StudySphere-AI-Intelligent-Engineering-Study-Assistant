"""Retrieval-Augmented Generation (RAG) Engine with Chromadb."""
from typing import List, Dict, Optional


class RAGEngine:
    """Implement RAG pattern for question answering."""

    def __init__(self, ai_service, vector_db):
        """Initialize RAG engine.
        
        Args:
            ai_service: AIService instance for generating responses
            vector_db: VectorDB instance (Chromadb-based)
        """
        self.ai_service = ai_service
        self.vector_db = vector_db

    def retrieve_context(self, query: str, k: int = 5) -> List[str]:
        """Retrieve relevant context documents for a query.
        
        Args:
            query: Search query string
            k: Number of documents to retrieve (default: 5)
            
        Returns:
            List of relevant document texts
        """
        try:
            # Chromadb handles embedding internally
            documents, distances = self.vector_db.search(query, k=k)
            return documents
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []

    def generate_answer(
        self, 
        query: str, 
        context: List[str], 
        sources: Optional[List[str]] = None
    ) -> Dict:
        """Generate answer using retrieved context.
        
        Args:
            query: User question
            context: List of relevant context documents
            sources: Optional list of source references
            
        Returns:
            Dictionary with answer, sources, and context metadata
        """
        context_str = "\n\n".join(context)
        prompt = f"""Based on the following context, answer the question:

Context:
{context_str}

Question: {query}

Provide a clear and accurate answer based solely on the context provided."""

        try:
            answer = self.ai_service.generate_response(prompt)
        except Exception as e:
            answer = f"Error generating answer: {str(e)}"

        return {
            "answer": answer,
            "sources": sources or [],
            "context_used": len(context),
            "context_documents": context,
        }

    def retrieve_and_answer(
        self, 
        query: str, 
        k: int = 5,
        sources: Optional[List[str]] = None
    ) -> Dict:
        """End-to-end RAG: retrieve context and generate answer.
        
        Args:
            query: User question
            k: Number of context documents to retrieve
            sources: Optional source references
            
        Returns:
            Dictionary with complete RAG response
        """
        context = self.retrieve_context(query, k=k)
        return self.generate_answer(query, context, sources)
