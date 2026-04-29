# 🧠 Curio AI — Role-Reversal Learning Platform

**Learn by teaching.** Curio AI flips the script: instead of an AI teaching you, *you* teach the AI. Curio acts as a curious student — asking questions, challenging your logic, catching mistakes, and evaluating how well you understand the topic.

Based on the **Feynman Technique** and the **Protégé Effect**: teaching is the deepest form of learning.

---

## 🏗 Architecture

```
Client → Routes (HTTP + validation) → Services (business logic) → AI Provider → Response
```

| Layer | Purpose |
|-------|---------|
| **Routes** | Thin HTTP controllers — validation only |
| **Services** | Business logic, orchestration |
| **Models** | Pydantic request/response schemas |
| **Config** | Environment + constants |
| **Utils** | Logging, errors, helpers |

### Key Design Decisions
- **AI Provider Abstraction**: `AIClient` protocol — swap OpenAI/Gemini/local without touching routes
- **Pluggable Evaluation**: Rule-based now, AI-based later — same interface
- **Session Store Interface**: In-memory now, Redis/PostgreSQL later
- **Consistent Envelope**: Every response uses `ResponseEnvelope { success, data, error, request_id }`

---

## 🚀 Quick Start

### 1. Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
```

### 2. Run
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Verify
```bash
curl http://localhost:8000/health
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/session/create` | Create teaching session |
| `GET` | `/api/session/{id}` | Get session state |
| `POST` | `/api/chat` | Send teaching message |
| `POST` | `/api/evaluate` | Evaluate teaching performance |
| `POST` | `/api/report` | Generate learning report |

### Example Flow (curl)

```bash
# 1. Create a session
curl -X POST http://localhost:8000/api/session/create \
  -H "Content-Type: application/json" \
  -d '{"topic": "Photosynthesis", "user_id": "student-1"}'

# 2. Teach the AI (use session_id from step 1)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess-XXXX", "user_message": "Photosynthesis is the process by which plants convert sunlight into energy. For example, leaves absorb CO2 and water..."}'

# 3. Evaluate (after 3+ teaching turns)
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess-XXXX"}'

# 4. Generate report
curl -X POST http://localhost:8000/api/report \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess-XXXX"}'
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV` | `dev` | Environment (dev/staging/prod) |
| `AI_PROVIDER` | `mock` | AI provider: `mock`, `openai`, `gemini` |
| `AI_MODEL` | `mock-v1` | Model identifier |
| `SESSION_TTL_MINUTES` | `60` | Session expiry time |
| `CORS_ORIGINS` | `[localhost]` | Allowed CORS origins |
| `LOG_LEVEL` | `INFO` | Logging level |

Set `AI_PROVIDER=mock` to run without API keys.

---

## 🧪 Test Strategy (Planned)

### Unit Tests (services/)
- `test_session_manager.py` — CRUD, TTL, expiry cleanup
- `test_input_processor.py` — sanitization, truncation, edge cases
- `test_evaluation_router.py` — scoring dimensions, edge cases
- `test_report_generator.py` — gap detection, drill suggestions

### Integration Tests (routes/)
- `test_session_routes.py` — create/get session lifecycle
- `test_chat_routes.py` — full chat flow with mock AI
- `test_evaluate_routes.py` — evaluation with sufficient turns
- `test_report_routes.py` — report generation after evaluation

---

## 🔮 Future Innovations
- [ ] Real AI providers (OpenAI, Gemini, local LLMs)
- [ ] AI-based evaluation (replace heuristics)
- [ ] Conversation summarization for long sessions
- [ ] Persistent storage (PostgreSQL + Redis)
- [ ] Multi-tenant support
- [ ] Spaced repetition scheduling
- [ ] Frontend application
