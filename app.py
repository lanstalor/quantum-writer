# app.py
from flask import Flask, render_template, request, redirect, url_for
from ai_interface import AIInterface
from context_manager import ContextManager
from story_manager import StoryManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
ai = AIInterface()  # Will use the API key from .env file
context_manager = ContextManager()
story_manager = StoryManager()

@app.route('/')
def index():
    return render_template('index.html', story=story_manager.story_data)

@app.route('/initialize', methods=['POST'])
def initialize_story():
    title = request.form.get('title')
    genre = request.form.get('genre')
    
    if not title:
        return redirect(url_for('index'))
    
    story_manager.initialize_story(title, genre)
    
    # Generate initial chapter with AI
    system_prompt = f"""You are an expert creative writer helping to create a {genre} novel titled '{title}'.
    Write an engaging opening chapter that establishes the setting, introduces key characters, and creates intrigue.
    Write in a professional, polished literary style appropriate for the genre.
    Your response should be a complete chapter of approximately 1500-2000 words."""
    
    initial_chapter = ai.generate_content(
        prompt=f"Write the opening chapter for a {genre} novel titled '{title}'.",
        context="",
        system_prompt=system_prompt
    )
    
    story_manager.add_chapter("Opening Chapter", initial_chapter)
    context_manager.update_context(initial_chapter)
    
    return redirect(url_for('view_story'))

@app.route('/story')
def view_story():
    return render_template('story.html', story=story_manager.story_data)

@app.route('/continue', methods=['POST'])
def continue_story():
    prompt = request.form.get('prompt', '')
    hidden_note = request.form.get('hidden_note', '')
    
    if hidden_note:
        context_manager.add_hidden_note(hidden_note)
    
    current_chapter = story_manager.get_current_chapter_number()
    
    # Create a system prompt that maintains narrative consistency
    system_prompt = f"""You are an expert creative writer helping to create the next chapter of an ongoing novel.
    Please continue the story based on all previous content and guidance provided.
    Maintain consistency with established characters, settings, and plot points.
    The new chapter should be approximately 1500-2000 words and flow naturally from previous content.
    If hidden guidance is provided in Chinese, follow those suggestions while keeping the narrative coherent."""
    
    # Get the next chapter from the AI
    next_chapter = ai.generate_content(
        prompt=prompt or "Continue the story with the next chapter. Develop the plot and characters further.",
        context=context_manager.get_full_context(),
        system_prompt=system_prompt
    )
    
    # Add the chapter to our story
    chapter_title = f"Chapter {current_chapter + 1}"
    story_manager.add_chapter(chapter_title, next_chapter)
    
    # Update our context
    context_manager.update_context(next_chapter)
    
    return redirect(url_for('view_story'))

@app.route('/analyze', methods=['GET'])
def analyze_story():
    # Use AI to analyze current story state
    system_prompt = """You are a literary analyst. Analyze the provided story and give insights on:
    1. Character development and arcs
    2. Plot threads and their status
    3. Current themes and motifs
    4. Pacing and narrative structure
    Your analysis should be constructive and focused on the story as written so far."""
    
    analysis = ai.generate_content(
        prompt="Provide a comprehensive analysis of the story so far.",
        context=context_manager.get_full_context(include_hidden_notes=False),
        system_prompt=system_prompt
    )
    
    return render_template('analysis.html', analysis=analysis, story=story_manager.story_data)

if __name__ == '__main__':
    app.run(debug=True)
