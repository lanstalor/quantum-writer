import os
from typing import List, Dict

import spacy
from ai_interface import AIInterface
from story_manager import StoryManager


class StoryInitializer:
    def __init__(self, context_dir: str = "context", ai_interface: AIInterface | None = None):
        self.context_dir = context_dir
        self.ai = ai_interface or AIInterface()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not installed; fall back to blank model
            self.nlp = spacy.blank("en")

    def load_story_files(self) -> str:
        """Load all text files from the context directory."""
        texts: List[str] = []
        for filename in os.listdir(self.context_dir):
            if filename.lower().endswith((".txt", ".md")):
                with open(os.path.join(self.context_dir, filename), "r", encoding="utf-8") as f:
                    texts.append(f.read())
        return "\n".join(texts)

    def analyze_story_content(self) -> Dict[str, List[str]]:
        """Extract basic story elements using spaCy."""
        text = self.load_story_files()
        doc = self.nlp(text)
        characters = set()
        locations = set()
        themes = set()

        for ent in doc.ents:
            if ent.label_ == "PERSON":
                characters.add(ent.text)
            elif ent.label_ in {"GPE", "LOC"}:
                locations.add(ent.text)
            elif ent.label_ in {"EVENT", "WORK_OF_ART"}:
                themes.add(ent.text)

        # Ask the AI for any additional insights
        ai_notes = self.ai.generate_content(
            prompt="Identify any additional key themes or narrative elements.",
            context=text,
            system_prompt="You are a helpful story analyst summarizing key elements from the text."
        )

        return {
            "characters": sorted(characters),
            "locations": sorted(locations),
            "themes": sorted(themes),
            "ai_notes": ai_notes.strip(),
        }

    def initialize_from_context(self, title: str | None = None, genre: str | None = None) -> Dict:
        """Create and save a new story initialized from context files."""
        analysis = self.analyze_story_content()
        manager = StoryManager()
        manager.initialize_story(title or "Untitled Story", genre or "Unknown")
        for name in analysis["characters"]:
            manager.update_character(name, {"name": name})
        manager.story_data["current_themes"] = analysis["themes"]
        manager.add_plot_thread("Initialized from context files")
        manager.save_story()
        return manager.story_data


if __name__ == "__main__":
    initializer = StoryInitializer()
    story = initializer.initialize_from_context()
    print("Initialized story:")
    print(story)
