"""AI/LLM service."""
from typing import List, Optional
import json


class AIService:
    """Handle AI operations using Google Gemini API."""

    def __init__(self, api_key: str):
        """Initialize AI service."""
        import google.generativeai as genai

        self.genai = genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_response(
        self, prompt: str, context: Optional[str] = None, temperature: float = 0.7
    ) -> str:
        """Generate response from LLM."""
        if context:
            full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"
        else:
            full_prompt = prompt

        response = self.model.generate_content(full_prompt)
        return response.text

    def generate_summary(self, text: str, summary_type: str = "short") -> str:
        """Generate summary of text."""
        if summary_type == "short":
            prompt = f"Provide a brief 2-3 sentence summary:\n\n{text}"
        elif summary_type == "detailed":
            prompt = f"Provide a detailed summary:\n\n{text}"
        elif summary_type == "bullet":
            prompt = f"Provide summary as bullet points:\n\n{text}"
        elif summary_type == "revision":
            prompt = f"Create an exam revision summary:\n\n{text}"
        else:
            prompt = f"Summarize:\n\n{text}"

        return self.generate_response(prompt)

    def generate_quiz_questions(self, text: str, num_questions: int = 10, difficulty: str = "medium") -> List[dict]:
        """Generate quiz questions from text."""
        prompt = f"""Generate {num_questions} quiz questions at {difficulty} level from the following text.
        
Return as JSON array with objects containing: question, type (mcq/true_false/fill_blank/short), options (for mcq), correct_answer, explanation.

Text:
{text}"""

        response = self.generate_response(prompt)
        try:
            # Parse JSON response
            import json
            questions = json.loads(response)
            return questions
        except json.JSONDecodeError:
            return []

    def generate_flashcards(self, text: str, num_cards: int = 10) -> List[dict]:
        """Generate flashcards from text."""
        prompt = f"""Generate {num_cards} flashcards from the following text.

Return as JSON array with objects containing: question, answer, difficulty.

Text:
{text}"""

        response = self.generate_response(prompt)
        try:
            flashcards = json.loads(response)
            return flashcards
        except json.JSONDecodeError:
            return []
