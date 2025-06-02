# Quantum Writer MVP Roadmap - 2 Day Sprint

## Objective
Transform the current skeleton implementation into a working AI-powered story generator that can:
- Create stories with AI-generated content
- Manage chapters with proper navigation
- Provide a simple but functional UI
- Save and retrieve user stories

## Day 1: Backend Implementation (Focus: AI & Story Management)

### Morning (4 hours)
1. **AI Service Implementation**
   - [ ] Port `ai_interface.py` logic to AI microservice
   - [ ] Create `/api/v1/generate` endpoint with proper request/response models
   - [ ] Implement streaming support for real-time generation
   - [ ] Add error handling and retry logic
   - [ ] Test with Anthropic API key

2. **Story Service - Chapter Management**
   - [ ] Implement `POST /api/v1/stories/{story_id}/chapters` - Create chapter
   - [ ] Implement `GET /api/v1/stories/{story_id}/chapters` - List chapters
   - [ ] Implement `GET /api/v1/chapters/{chapter_id}` - Get single chapter
   - [ ] Implement `PUT /api/v1/chapters/{chapter_id}` - Update chapter
   - [ ] Implement `DELETE /api/v1/chapters/{chapter_id}` - Delete chapter

### Afternoon (4 hours)
3. **Database Integration**
   - [ ] Set up Alembic migrations
   - [ ] Create initial migration for all models
   - [ ] Test database operations
   - [ ] Add proper error handling

4. **Integration Testing**
   - [ ] Test story creation flow
   - [ ] Test chapter generation with AI
   - [ ] Test data persistence
   - [ ] Fix any integration issues

## Day 2: Frontend & Integration (Focus: UI & User Experience)

### Morning (4 hours)
1. **Frontend - Story Management**
   - [ ] Create story list page (`/stories`)
   - [ ] Create new story form with title, genre, initial prompt
   - [ ] Implement story API client service
   - [ ] Add loading states and error handling

2. **Frontend - Chapter Editor**
   - [ ] Create chapter editor page (`/stories/[id]/edit`)
   - [ ] Build AI prompt interface component
   - [ ] Implement chapter navigation (prev/next)
   - [ ] Add auto-save functionality

### Afternoon (4 hours)
3. **Authentication & Security**
   - [ ] Implement JWT token generation in auth service
   - [ ] Add login/register endpoints
   - [ ] Create frontend auth pages
   - [ ] Protect API routes with auth middleware
   - [ ] Associate stories with users

4. **End-to-End Testing & Polish**
   - [ ] Complete user flow test: Register → Create Story → Generate Chapters → Navigate
   - [ ] Fix any UI/UX issues
   - [ ] Add basic styling and loading indicators
   - [ ] Ensure data persistence works correctly
   - [ ] Deploy and test in production-like environment

## Success Criteria
By end of Day 2, we should have:
- ✅ Users can register and login
- ✅ Users can create a new story with title and initial prompt
- ✅ AI generates story content based on prompts
- ✅ Users can generate multiple chapters
- ✅ Users can navigate between chapters
- ✅ All data persists in PostgreSQL
- ✅ Basic but functional UI

## Key Files to Create/Modify

### Day 1
- `/services/ai/app/api/v1/generate.py` - AI generation endpoint
- `/services/ai/app/services/anthropic_service.py` - Claude integration
- `/services/story/app/api/v1/chapters.py` - Chapter endpoints
- `/services/story/alembic/versions/` - Database migrations

### Day 2
- `/frontend/src/app/stories/page.tsx` - Story list
- `/frontend/src/app/stories/[id]/edit/page.tsx` - Chapter editor
- `/frontend/src/services/api.ts` - API client
- `/frontend/src/components/AIPrompt.tsx` - AI interface
- `/services/auth/app/api/v1/auth.py` - Auth endpoints

## Notes
- Keep it simple - no branching narratives, no real-time collaboration
- Focus on core flow: Create → Generate → Navigate → Save
- Use existing Flask app logic as reference
- Don't over-engineer - we can refactor later