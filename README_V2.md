# Quantum Writer 2.0

A professional-grade AI-assisted storytelling platform built with microservices architecture, real-time collaboration, and advanced narrative management capabilities.

## 🚀 Features

- **Multi-Model AI Integration**: Support for Claude, GPT-4, and Llama models
- **Real-time Collaboration**: Multiple authors can work together with live updates
- **Branching Narratives**: Explore alternative storylines and merge the best elements
- **Smart Context Management**: Vector embeddings and semantic search for narrative consistency
- **Advanced Analytics**: Story structure visualization, pacing analysis, and character tracking
- **Professional Export**: EPUB, PDF, and various writing software formats

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   Kong API  │────▶│  Services   │
│  Frontend   │     │   Gateway   │     │ (FastAPI)   │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                    ┌──────────────────────────┴───────────────┐
                    │                                          │
              ┌─────▼─────┐  ┌────────────┐  ┌────────────┐  │
              │PostgreSQL │  │   Redis    │  │  Qdrant    │  │
              │(Core DB)  │  │  (Cache)   │  │(Vector DB) │  │
              └───────────┘  └────────────┘  └────────────┘  │
```

### Services

- **Story Service**: CRUD operations, versioning, branching
- **AI Service**: LLM integration, prompt engineering, response streaming
- **Analysis Service**: NLP, character extraction, narrative analysis
- **Context Service**: Vector embeddings, semantic search, context optimization
- **Auth Service**: JWT authentication, RBAC, team management
- **WebSocket Service**: Real-time collaboration, live updates

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/lanstalor/quantum-writer.git
cd quantum-writer
```

2. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Start the development environment:
```bash
make setup  # First time only
make dev    # Start all services
```

4. Access the application:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## 🛠️ Development

### Project Structure

```
quantum-writer/
├── frontend/               # Next.js 14 application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── features/      # Feature modules
│   │   ├── hooks/         # Custom hooks
│   │   └── lib/           # Utilities
│   └── package.json
├── services/              # Microservices
│   ├── story/            # Story management
│   ├── ai/               # AI integration
│   ├── analysis/         # Story analysis
│   ├── context/          # Context management
│   ├── auth/             # Authentication
│   └── websocket/        # Real-time features
├── infrastructure/        # Deployment configs
│   ├── docker/
│   └── kubernetes/
└── docs/                  # Documentation
```

### Common Commands

```bash
# Development
make dev        # Start all services
make stop       # Stop all services
make logs       # View logs

# Testing
make test       # Run all tests
make lint       # Lint code

# Database
make migrate    # Run migrations

# Cleanup
make clean      # Remove containers and volumes
```

### Adding a New Feature

1. Create feature branch:
```bash
git checkout -b feature/your-feature
```

2. Implement the feature following the architecture:
   - Backend: Add endpoint to relevant service
   - Frontend: Create feature module in `/src/features/`
   - Database: Add migration if needed

3. Write tests:
   - Backend: pytest in service directory
   - Frontend: Jest tests alongside components

4. Submit PR with:
   - Description of changes
   - Test results
   - Migration steps (if applicable)

## 🧪 Testing

### Backend Tests
```bash
cd services/story
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📚 API Documentation

Once services are running, access interactive API docs:

- Story Service: http://localhost:8010/api/docs
- AI Service: http://localhost:8011/api/docs
- Analysis Service: http://localhost:8012/api/docs
- Context Service: http://localhost:8013/api/docs
- Auth Service: http://localhost:8014/api/docs

## 🚀 Deployment

### Production Build

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

```bash
kubectl apply -f infrastructure/kubernetes/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes with conventional commits
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI, Next.js, and PostgreSQL
- AI powered by Anthropic Claude, OpenAI, and Meta Llama
- Vector search by Qdrant/Pinecone
- Real-time collaboration with Yjs

## 📞 Support

- Documentation: See `/docs` directory
- Issues: GitHub Issues
- Discussions: GitHub Discussions