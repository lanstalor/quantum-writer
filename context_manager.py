# context_manager.py
from typing import List, Dict, Any
import json

class ContextManager:
    def __init__(self, max_tokens: int = 90000):
        self.max_tokens = max_tokens
        self.current_context = ""
        self.character_summaries = {}
        self.plot_points = []
        self.themes = []
        self.hidden_notes = []  # For author guidance (stored in Chinese)
        
    def update_context(self, new_content: str) -> None:
        """Add new content to context while managing size"""
        # Simple approach: keep full recent content, summarize older content
        self.current_context += f"\n\n{new_content}"
        self._optimize_context_size()
        
    def add_hidden_note(self, note: str) -> None:
        """Add hidden guidance note for future context"""
        self.hidden_notes.append(note)
        
    def _optimize_context_size(self) -> None:
        """Ensure context stays within token limit"""
        # Very simple approach: if too large, keep recent sections and summaries
        estimated_tokens = len(self.current_context.split()) * 1.3  # Rough estimation
        
        if estimated_tokens > self.max_tokens:
            # Split into sections and keep most recent
            sections = self.current_context.split("\n\n")
            
            # Keep character summaries and recent sections
            preserved = "\n\n".join(sections[-30:])  # Keep most recent sections
            
            # Convert older sections to summaries (in practice, you'd use AI here)
            self.current_context = (
                "STORY SUMMARY (EARLIER CHAPTERS):\n" + 
                "[Summary would be generated here]\n\n" +
                "CHARACTER INFORMATION:\n" + 
                json.dumps(self.character_summaries, indent=2) + "\n\n" +
                "RECENT STORY CONTENT:\n" + preserved
            )
            
    def get_full_context(self, include_hidden_notes: bool = True) -> str:
        """Return optimized context for AI prompt"""
        context = self.current_context
        
        if include_hidden_notes and self.hidden_notes:
            notes = "\n".join(self.hidden_notes)
            context += f"\n\n隐藏指导 (HIDDEN GUIDANCE):\n{notes}"
            
        return context
