# 🎭 Curio AI — A Role Reversal AI Engine

> **The AI that learns from you.**
>
> Curio AI flips traditional learning upside down: instead of AI teaching students, **students teach the AI**.
>
> Inspired by the **Feynman Technique** and the **Protégé Effect**, Curio acts as an intelligent student—asking questions, challenging explanations, identifying gaps, and evaluating understanding.

---

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Backend-FastAPI-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/AI-Provider_Agnostic-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

---

## 🧠 Why Curio AI?

Most learning platforms focus on **consuming information**.

Curio focuses on **explaining information**.

Research consistently shows that teaching others dramatically improves understanding. Curio transforms this principle into an AI-powered learning experience.

### The Learning Loop

```text
Learn → Explain → Defend → Correct → Master
```

When teaching Curio:

* 🗣 Explain concepts in your own words
* ❓ Answer follow-up questions
* 🧩 Fill knowledge gaps
* ⚡ Correct misconceptions
* 📈 Strengthen long-term retention

---

# ✨ Core Features

### 🎓 AI Student Roleplay

Curio behaves like an inquisitive learner rather than an instructor.

### 🧠 Socratic Questioning

The AI asks clarification and challenge questions to deepen understanding.

### 🔍 Gap Detection

Identifies missing explanations and weak reasoning.

### 📊 Learning Evaluation

Measures clarity, completeness, examples, and conceptual depth.

### 📄 Personalized Reports

Generates actionable feedback and improvement suggestions.

### 🔌 Provider Agnostic AI

Swap between OpenAI, Gemini, or local LLMs seamlessly.

---

# 🏗 System Architecture

```text
┌──────────┐
│  Client  │
└────┬─────┘
     │ HTTP
     ▼
┌──────────────┐
│    Routes    │
│ Validation   │
└────┬─────────┘
     ▼
┌──────────────┐
│   Services   │
│ Business     │
│ Logic        │
└────┬─────────┘
     ▼
┌──────────────┐
│ AI Provider  │
│ Abstraction  │
└────┬─────────┘
     ▼
┌──────────────┐
│ Response API │
└──────────────┘
```

---

## 📂 Project Structure

```bash
backend/
│
├── app/
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   ├── models/        # Pydantic schemas
│   ├── providers/     # AI providers
│   ├── utils/         # Helpers & logging
│   ├── config/        # Settings
│   └── main.py
│
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙️ Design Principles

## 🔄 AI Provider Abstraction

```python
class AIClient(Protocol):
    async def generate_response(...):
        ...
```

Switch providers without touching business logic.

Supported:

* Mock AI
* OpenAI
* Gemini
* Local LLMs (Future)

---

## 🧩 Pluggable Evaluation Engine

Current:

* Rule-based heuristics

Future:

* LLM-powered evaluation
* Semantic scoring
* Knowledge graph comparison

---

## 🗄 Session Store Interface

Current:

* In-memory storage

Future:

* Redis
* PostgreSQL
* Distributed caching

---

## 📦 Unified Response Envelope

Every API response follows:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "request_id": "req_123"
}
```

This ensures consistency across all endpoints.

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd backend
```

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Configure Environment

```bash
cp .env.example .env
```

Example:

```env
ENV=dev
AI_PROVIDER=mock
AI_MODEL=mock-v1
SESSION_TTL_MINUTES=60
LOG_LEVEL=INFO
```

> Use `AI_PROVIDER=mock` to run Curio without API keys.

---

## 5️⃣ Run Server

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 6️⃣ Verify API

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 📡 REST API

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| GET    | `/health`             | Health check      |
| POST   | `/api/session/create` | Create session    |
| GET    | `/api/session/{id}`   | Retrieve session  |
| POST   | `/api/chat`           | Teach Curio       |
| POST   | `/api/evaluate`       | Evaluate teaching |
| POST   | `/api/report`         | Generate report   |

---

# 🔄 Example Workflow

## 1. Create Session

```bash
curl -X POST http://localhost:8000/api/session/create \
-H "Content-Type: application/json" \
-d '{
  "topic":"Photosynthesis",
  "user_id":"student-1"
}'
```

---

## 2. Teach Curio

```bash
curl -X POST http://localhost:8000/api/chat \
-H "Content-Type: application/json" \
-d '{
  "session_id":"sess-XXXX",
  "user_message":"Photosynthesis converts sunlight into chemical energy."
}'
```

---

## 3. Evaluate Learning

```bash
curl -X POST http://localhost:8000/api/evaluate \
-H "Content-Type: application/json" \
-d '{
  "session_id":"sess-XXXX"
}'
```

---

## 4. Generate Report

```bash
curl -X POST http://localhost:8000/api/report \
-H "Content-Type: application/json" \
-d '{
  "session_id":"sess-XXXX"
}'
```

---

# 📈 Evaluation Metrics

Curio scores explanations across:

| Dimension    | Description              |
| ------------ | ------------------------ |
| Clarity      | Easy to understand       |
| Completeness | Covers all concepts      |
| Examples     | Real-world analogies     |
| Accuracy     | Correct information      |
| Depth        | Conceptual understanding |

---

# 🧪 Testing Strategy

## Unit Tests

```text
test_session_manager.py
test_input_processor.py
test_evaluation_router.py
test_report_generator.py
```

## Integration Tests

```text
test_session_routes.py
test_chat_routes.py
test_evaluate_routes.py
test_report_routes.py
```

Run tests:

```bash
pytest
```

---

# 🔮 Future Roadmap

* [ ] OpenAI Integration
* [ ] Gemini Integration
* [ ] Local LLM Support
* [ ] AI-powered Evaluation
* [ ] Redis Session Storage
* [ ] PostgreSQL Persistence
* [ ] Conversation Summarization
* [ ] Spaced Repetition System
* [ ] Multi-Tenant Support
* [ ] Frontend Dashboard
* [ ] Learning Analytics
* [ ] Voice-Based Teaching

---

# 🌟 Vision

> *"The best way to learn is to teach."*

Curio AI aims to become the world's first **AI-powered teaching companion**, transforming passive learners into active teachers.

By reversing the traditional AI-student relationship, Curio unlocks deeper understanding, stronger retention, and true mastery.

---

<p align="center">
Built with ❤️ using FastAPI, Pydantic and AI.
</p>
