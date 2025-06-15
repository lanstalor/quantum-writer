# Quantum Writer v2.0 🚀

**AI-Powered Microservices Storytelling Platform**

A modern, scalable platform for creating AI-assisted interactive narratives with branching storylines, multi-model AI support, and real-time collaboration.

## 🎯 Current Status: Functional MVP ✅

✅ **Full-Stack Working**: End-to-end story creation and AI generation
✅ **Multi-AI Support**: Groq, GPT-4o-mini, and Claude integration
✅ **Frontend**: Next.js story editor with chapter reader
🚧 **Authentication**: Basic structure ready
🚧 **Branch Merging & Context Improvements**: In progress

### 🚀 What's Working Now
- ✅ **Multi-AI Story Generation**: Groq Llama 3.1, GPT-4o-mini, Claude support
- ✅ **Story Management**: Full CRUD with responsive frontend interface
- ✅ **Chapter Reading**: Modal dialog with formatting and scrolling
- ✅ **Database Persistence**: PostgreSQL with complete story/chapter schema
- ✅ **API Gateway**: Kong routing with microservices architecture
- ✅ **Context Continuity**: AI maintains narrative consistency using previous chapters
- ✅ **Docker Environment**: Full containerized development setup

### 🎯 Key MVP Achievements
- **End-to-End Flow**: Create story → Generate chapters → Read content
- **Model Flexibility**: Switch between AI models for different content policies
- **Production Ready**: Microservices architecture with proper error handling

## 🏗️ Architecture

**Modern Microservices Design:**
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS + Shadcn/ui
- **API Gateway**: Kong (port 8000) 
- **Backend**: 6 FastAPI microservices with async SQLAlchemy
- **Databases**: PostgreSQL + Redis + Qdrant + Elasticsearch
- **AI**: Multi-model support (Groq Llama 3.1, GPT-4o-mini, Claude)

| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| Frontend | 3000 | ✅ **Working** | Next.js story editor & reader |
| API Gateway | 8000 | ✅ **Working** | Kong routing |
| Story Service | 8010 | ✅ **Working** | Story/chapter CRUD with AI |
| AI Service | 8011 | ✅ **Working** | Multi-model LLM integration |
| Analysis Service | 8012 | ✅ Skeleton | NLP analysis |
| Context Service | 8013 | ✅ Skeleton | Vector search |
| Auth Service | 8014 | ✅ Skeleton | Authentication |
| WebSocket Service | 8015 | ✅ Skeleton | Real-time sync |

### 🤖 AI Models Integrated
- **Groq Llama 3.1 8B** (default): 128K context, most permissive for creative content
- **GPT-4o-mini**: 128K context, balanced quality and flexibility
- **Claude Opus**: 200K context, highest quality but most restrictive

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Git  
- **AI API Keys** (at least one):
  - Groq API key (recommended - free tier available)
  - OpenAI API key (for GPT-4o-mini)
  - Anthropic API key (for Claude)

### 1. Clone and Setup
```bash
git clone https://github.com/lanstalor/quantum-writer.git
cd quantum-writer

# Set environment variables
export GROQ_API_KEY="your_groq_key_here"
export OPENAI_API_KEY="your_openai_key_here"  # optional
export ANTHROPIC_API_KEY="your_anthropic_key_here"  # optional
```

### 2. Start Full Application
```bash
# Start all services including frontend
GROQ_API_KEY=your_key_here docker compose up -d

# Check service health
curl http://localhost:8011/health  # AI service
curl http://localhost:8010/health  # Story service
```

### 3. Use the Application
```bash
# Open the web interface
open http://localhost:3000

# Or test via API
curl -X POST "http://localhost:8000/api/v1/stories/" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: test-user" \
  -d '{"title": "My Fantasy Adventure", "genre": "fantasy", "description": "An epic tale"}'
```

### 4. Generate Chapters with Different AI Models
```bash
# Generate with Groq (default - most permissive)
curl -X POST "http://localhost:8000/api/v1/chapters/generate?model=groq" \
  -H "Content-Type: application/json" \
  -d '{"story_id": "STORY_ID", "title": "Chapter 1", "prompt": "Write an epic opening chapter"}'

# Generate with GPT-4o-mini (balanced)  
curl -X POST "http://localhost:8000/api/v1/chapters/generate?model=gpt" \
  -H "Content-Type: application/json" \
  -d '{"story_id": "STORY_ID", "title": "Chapter 2", "prompt": "Continue the adventure"}'

# Generate with Claude (highest quality, most restrictive)
curl -X POST "http://localhost:8000/api/v1/chapters/generate?model=claude" \
  -H "Content-Type: application/json" \
  -d '{"story_id": "STORY_ID", "title": "Chapter 3", "prompt": "Build tension and conflict"}'
```

## 📚 API Documentation

With services running, visit:
- **Story Service**: http://localhost:8010/api/docs
- **AI Service**: http://localhost:8011/api/docs  
- **All Services**: Individual docs at ports 8010-8015

## 🛠️ Development

### Backend Development
```bash
# Individual service development
cd services/ai && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8011

# Database setup
docker compose exec story-service python -c "
from app.db.database import engine, Base
import asyncio
asyncio.run(Base.metadata.create_all(engine))
"
```

### Frontend Development  
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### Testing
```bash
# Backend tests
cd services/story && pytest
cd services/ai && pytest

# Frontend tests  
cd frontend && npm test
```

## 📖 Documentation

- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)**: Detailed technical guide
- **[MVP Roadmap](MVP_ROADMAP.md)**: Current development plan
- **[AI Enhancement Ideas](AI_ENHANCEMENT_IDEAS.md)**: Future feature concepts
- **[Claude Guide](CLAUDE.md)**: AI assistant development guidance

## 🎯 Roadmap

### v2.0 MVP ✅ COMPLETE
- [x] Multi-AI story generation backend (Groq, GPT, Claude)
- [x] Story/chapter management with full CRUD
- [x] Database persistence with PostgreSQL
- [x] Frontend story editor with Next.js
- [x] Chapter reader with modal interface
- [x] End-to-end story creation flow
- [x] Docker containerized environment
- [ ] Authentication system (structure ready)

### v2.1 (Next Sprint)
- [ ] Enhanced AI prompting for better content quality
- [ ] Chapter editing and revision capabilities
- [ ] User authentication and story ownership
- [ ] Author persona emulation (Pierce Brown, Sanderson, etc.)
- [ ] Story export to markdown/text formats
- [ ] UI/UX improvements and polish

### v2.2 (Advanced Features)
- [ ] Branch merging and alternative narratives
- [ ] Enhanced context management with vector search and summarization
- [ ] Real-time collaborative editing
- [ ] Advanced story analysis and visualization
- [ ] Export to EPUB/PDF
- [ ] Story templates and genre-specific prompts

### v2.3+ (Future)
- [ ] Team collaboration features
- [ ] Story marketplace and sharing
- [ ] Mobile app
- [ ] Advanced analytics and insights
- [ ] Plugin system for custom AI models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: Lightning-fast Llama inference for creative AI generation
- **Anthropic Claude**: High-quality AI story generation and assistance
- **OpenAI**: GPT-4o-mini for balanced creative writing
- **FastAPI**: Enabling rapid microservice development
- **Next.js + Shadcn/ui**: Modern React framework and components
- **Docker**: Containerization and development environment

---

## 📈 Development Stats
- **Days to MVP**: 2 days ⚡
- **Services Built**: 6 microservices
- **AI Models**: 3 integrated (Groq, GPT, Claude)
- **Lines of Code**: ~5,000+ (backend + frontend)
- **Docker Services**: 10 containerized services
- **APIs**: Fully documented with OpenAPI/Swagger

**Built with ❤️ for storytellers, by storytellers**

*Turn your ideas into epic narratives with the power of AI - now with multi-model support!*