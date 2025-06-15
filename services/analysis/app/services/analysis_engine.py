import re
from typing import List, Dict

class AnalysisEngine:
    """Simple NLP routines for story analysis."""

    @staticmethod
    def extract_characters(text: str) -> List[str]:
        """Return a list of unique capitalized names found in the text."""
        words = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", text)
        seen = set()
        characters: List[str] = []
        for w in words:
            if w not in seen:
                seen.add(w)
                characters.append(w)
        return characters

    @staticmethod
    def analyze_plot(text: str) -> Dict[str, object]:
        """Return a naive plot summary using the first and last sentences."""
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        if not sentences:
            return {"summary": ""}
        summary = sentences[0]
        if len(sentences) > 1:
            summary += " ... " + sentences[-1]
        return {"summary": summary, "sentence_count": len(sentences)}
