# AI Development Guide for Quantum Writer 2.0

## Project Overview
Quantum Writer is an AI-assisted storytelling platform for creating complex narratives with advanced context management, collaborative features, and intelligent story analysis.

## Current State (Legacy)
- Basic Flask app with simple file storage
- Claude API integration for story generation
- Rudimentary context management
- Single-user, single-story design

## Target Architecture

### Backend Microservices (FastAPI)
1. **Story Service**: CRUD operations, versioning, branching narratives
2. **AI Service**: Multi-model LLM integration (Claude, GPT-4, Llama)
3. **Analysis Service**: NLP, character extraction, plot analysis
4. **Context Service**: Vector embeddings, semantic search, smart retrieval
5. **Auth Service**: JWT-based auth, RBAC, team management
6. **Websocket Service**: Real-time collaboration, live updates

### Frontend (Next.js 14)
- Modern React with TypeScript
- Real-time collaborative editor (Lexical/Tiptap)
- Interactive visualizations (D3.js)
- Responsive design with Tailwind CSS
- PWA capabilities

### Data Layer
- PostgreSQL 15: Core data, versioning
- Redis 7: Caching, sessions, pub/sub
- Pinecone/Pgvector: Vector embeddings
- Elasticsearch 8: Full-text search
- S3/R2: File storage, exports

## Implementation Priorities

### Phase 1: Foundation
1. Set up Docker development environment
2. Create FastAPI microservices structure
3. Implement PostgreSQL schema with Alembic migrations
4. Build JWT authentication system
5. Create basic Next.js frontend with Shadcn/ui

### Phase 2: Core Features
1. Implement vector database integration
2. Build LangChain-based AI orchestration
3. Create collaborative editing with Yjs
4. Develop story analysis engine
5. Add real-time synchronization

### Phase 3: Advanced Features
1. Branching narrative system
2. Multi-model AI support
3. Story visualization tools
4. Plugin architecture
5. Mobile applications

## Key Technical Decisions

### API Design
```python
# RESTful + GraphQL hybrid
# REST for CRUD operations
# GraphQL for complex queries
# WebSockets for real-time

# Example endpoint structure:
/api/v1/stories
/api/v1/stories/{id}/chapters
/api/v1/stories/{id}/branches
/api/v1/analysis/{story_id}
/api/v1/ai/generate
/api/v1/ai/analyze
```

### Database Schema
```sql
-- Core tables
stories (id, title, genre, created_by, created_at, metadata)
chapters (id, story_id, branch_id, content, position, metadata)
branches (id, story_id, parent_branch_id, name, status)
characters (id, story_id, name, description, embeddings)
users (id, email, name, settings)
teams (id, name, owner_id)

-- Versioning
story_versions (id, story_id, version, changes, created_at)
chapter_versions (id, chapter_id, version, content, created_at)
```

### AI Integration Pattern
```python
class AIOrchestrator:
    def __init__(self):
        self.models = {
            'claude': ClaudeAdapter(),
            'gpt4': GPT4Adapter(),
            'llama': LlamaAdapter()
        }
        self.langchain = LangChainPipeline()
    
    async def generate(self, request: GenerateRequest):
        # Smart model selection
        # Context optimization
        # Response streaming
        # Error handling with fallbacks
```

## Development Guidelines

### Code Standards
- Python: Black formatter, Ruff linter, type hints
- TypeScript: ESLint, Prettier, strict mode
- Testing: pytest (80% coverage), Jest, Playwright
- Documentation: docstrings, OpenAPI, Storybook

### Git Workflow
```bash
main → develop → feature/xxx
# Feature branches from develop
# PRs require review + passing tests
# Semantic versioning
# Conventional commits
```

### Environment Setup
```bash
# Required tools
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Redis 7

# Development commands
make dev        # Start all services
make test       # Run test suite
make migrate    # Run DB migrations
make lint       # Lint codebase
```

## Security Considerations
1. JWT tokens with refresh rotation
2. Rate limiting per user/endpoint
3. Input validation with Pydantic
4. SQL injection prevention via ORM
5. XSS protection in React
6. CORS configuration
7. Secrets management with Vault

## Performance Targets
- API response time: <200ms (p95)
- Real-time sync latency: <100ms
- AI generation: streaming response
- Page load time: <2s
- Database queries: <50ms

## Monitoring & Observability
- Sentry for error tracking
- Prometheus + Grafana for metrics
- ELK stack for logs
- OpenTelemetry for tracing
- Custom dashboards for story analytics

## Deployment Strategy
```yaml
# Kubernetes deployment
- Blue/green deployments
- Horizontal pod autoscaling
- Service mesh (Istio)
- GitOps with ArgoCD
- Multi-region support
```

## AI-Specific Instructions

When implementing new features:
1. Always consider token limits and implement chunking
2. Use streaming responses for better UX
3. Implement retry logic with exponential backoff
4. Cache AI responses where appropriate
5. Provide fallbacks for AI failures
6. Monitor API costs and optimize

For context management:
1. Use hierarchical summarization
2. Implement semantic search with embeddings
3. Maintain character/location/theme indices
4. Track narrative consistency
5. Enable context templates

## Common Pitfalls to Avoid
1. Don't store large texts in PostgreSQL - use object storage
2. Don't block on AI calls - use async/streaming
3. Don't trust user input - validate everything
4. Don't forget rate limiting - implement early
5. Don't neglect testing - aim for 80% coverage

## Quick Start for New Features
```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Implement with tests
# Backend: /services/your-service/
# Frontend: /frontend/src/features/

# 3. Update documentation
# API docs: /docs/api/
# User docs: /docs/user/

# 4. Create PR with:
# - Description of changes
# - Test results
# - Performance impact
# - Migration steps (if needed)
```

## Contact & Resources
- Architecture diagrams: /docs/architecture/
- API documentation: /docs/api/
- Deployment guide: /docs/deployment/
- Original vision: /IMPLEMENTATION_GUIDE.md

Remember: The goal is to create a professional-grade platform that empowers authors while maintaining the innovative features like hidden guidance and probabilistic narratives that make Quantum Writer unique.