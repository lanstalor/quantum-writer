# story_manager.py
import json
import os
import datetime
from typing import Dict, Any, List

class StoryManager:
    def __init__(self, story_dir: str = "data"):
        self.story_dir = story_dir
        self.story_data = {
            "metadata": {
                "title": "",
                "genre": "",
                "created_at": "",
                "last_updated": "",
                "word_count": 0
            },
            "chapters": [],
            "characters": {},
            "plot_threads": [],
            "current_themes": []
        }
        self._ensure_directory()
        self._load_story()
        
    def _ensure_directory(self) -> None:
        """Make sure the story directory exists"""
        os.makedirs(self.story_dir, exist_ok=True)
        
    def _load_story(self) -> None:
        """Load story data if it exists"""
        story_path = os.path.join(self.story_dir, "story.json")
        if os.path.exists(story_path):
            with open(story_path, "r") as f:
                self.story_data = json.load(f)
                
    def save_story(self) -> None:
        """Persist story data to disk"""
        self.story_data["metadata"]["last_updated"] = datetime.datetime.now().isoformat()
        
        # Update word count
        words = 0
        for chapter in self.story_data["chapters"]:
            words += len(chapter["content"].split())
        self.story_data["metadata"]["word_count"] = words
        
        with open(os.path.join(self.story_dir, "story.json"), "w") as f:
            json.dump(self.story_data, f, indent=2)
            
    def initialize_story(self, title: str, genre: str) -> None:
        """Set up a new story"""
        self.story_data["metadata"]["title"] = title
        self.story_data["metadata"]["genre"] = genre
        self.story_data["metadata"]["created_at"] = datetime.datetime.now().isoformat()
        self.save_story()
        
    def add_chapter(self, title: str, content: str) -> None:
        """Add a new chapter to the story"""
        chapter = {
            "number": len(self.story_data["chapters"]) + 1,
            "title": title,
            "content": content,
            "created_at": datetime.datetime.now().isoformat()
        }
        self.story_data["chapters"].append(chapter)
        self.save_story()
        
    def update_character(self, name: str, details: Dict[str, Any]) -> None:
        """Update character information"""
        self.story_data["characters"][name] = details
        self.save_story()
        
    def add_plot_thread(self, description: str, status: str = "active") -> None:
        """Track a new plot thread"""
        thread = {
            "description": description,
            "status": status,
            "created_at": datetime.datetime.now().isoformat()
        }
        self.story_data["plot_threads"].append(thread)
        self.save_story()
        
    def get_current_chapter_number(self) -> int:
        """Get the current chapter number"""
        return len(self.story_data["chapters"])
        
    def get_full_story_text(self) -> str:
        """Return the full story text"""
        chapters = []
        for chapter in self.story_data["chapters"]:
            chapters.append(f"Chapter {chapter['number']}: {chapter['title']}\n\n{chapter['content']}")
        return "\n\n".join(chapters)