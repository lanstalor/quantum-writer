# Quantum Writer

An AI-assisted storytelling tool for creating and managing complex narrative structures with probabilistic storylines.

## Features

- AI-powered story generation and continuation
- Automated story analysis
- Context management for long narratives
- Character and plot tracking
- Hidden instruction generation in Chinese

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/quantum-writer.git
cd quantum-writer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

1. Run the web application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Initialize a new story or continue an existing one

## Project Structure

- `app.py`: Flask web application
- `ai_interface.py`: Claude API integration
- `context_manager.py`: Story context management
- `story_manager.py`: Story state and persistence
- `initialize_story.py`: Story setup and analysis
- `context/`: Sample story content
- `templates/`: Web UI templates
- `data/`: Saved story data

## Dependencies

- Flask
- Anthropic Claude API
- NLTK
- spaCy
- Python 3.8+ 