# Instructions for Quantum Writer Implementation

## Current Status
- Basic project structure created with app.py, ai_interface.py, context_manager.py, story_manager.py
- Sample story content in context folder (Quantum Anomaly)
- Project dependencies specified in requirements.txt
- Git repository initialized and pushed to GitHub

## Implementation Priorities

1. **Story Initialization System**
   - Implement `initialize_story.py` to analyze existing content files
   - Extract characters, themes, locations, and plot elements using NLP (spaCy/NLTK)
   - Add AI-enhanced analysis of story structure using Claude API

2. **Hidden Instruction Generator**
   - Enhance context_manager.py to automatically generate narrative guidance in Chinese
   - Implement analysis of current story state and progression
   - Ensure hidden instructions are included in context for future AI interactions

3. **Robust Error Handling**
   - Update ai_interface.py with retry logic for API failures
   - Implement token limit management and chunking for long contexts
   - Add appropriate user feedback for different error states

4. **Context Management Enhancements**
   - Implement vectorization of story segments for better retrieval
   - Add summarization capabilities to maintain coherence in long stories
   - Create a system to prioritize recent content while preserving important earlier elements

5. **Story Analysis Component**
   - Build automated character/plot/theme tracking based on generated content
   - Implement a visualization system for narrative structure
   - Add consistency checking to flag potential narrative contradictions

## Getting Started

Start with implementing `initialize_story.py` as it forms the foundation for the other enhancements. Test with the Quantum Anomaly sample content to verify proper extraction of story elements.

### Key Implementation Details

#### Story Initialization
```python
# Sample code structure for initialize_story.py
class StoryInitializer:
    def __init__(self, context_dir="context", ai_interface=None):
        self.context_dir = context_dir
        self.ai_interface = ai_interface or AIInterface()
        
    def load_story_files(self):
        # Load all .txt and .md files from context_dir
        
    def analyze_story_content(self):
        # Extract characters, locations, themes using NLP
        # Use AI to enhance analysis
        
    def initialize_from_context(self, title=None, genre=None):
        # Create new story based on existing content
```

#### Hidden Instruction Generation
```python
# Enhancement to context_manager.py
def generate_hidden_guidance(self, current_story_state):
    # Analyze current story state
    # Generate guidance in Chinese
    # Add to hidden_notes
```

#### API Error Handling
```python
# Enhancement to ai_interface.py
def generate_content_with_retry(self, prompt, context, system_prompt, max_retries=3):
    # Implement retry logic
    # Handle token limits
    # Return appropriate error messages
```

Test thoroughly with the Quantum Anomaly samples before proceeding to each subsequent enhancement. 