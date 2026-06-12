<div align="center">

# 🎭 Curio AI

### *Learn by Teaching. Master by Explaining.*

> **Don't learn from AI — teach it.**

Curio transforms learners into teachers by making AI play the role of an inquisitive student.

Inspired by the **Feynman Technique** and the **Protégé Effect**, Curio helps users discover knowledge gaps, strengthen understanding, and truly master concepts.

---

[Features](#-features) •
[Architecture](#-architecture) •
[API](#-api-endpoints) •
[Getting Started](#-getting-started) •
[Roadmap](#-roadmap)

</div>

---

# 🧠 The Problem

Traditional learning is often passive:

- Reading notes 📖
- Watching videos 🎥
- Memorizing facts 📝

But research shows that **teaching** is one of the most effective ways to learn.

The challenge?

Most learners don't have someone to teach.

Curio solves this by turning AI into an active student that learns from you.

---

# 🚀 How Curio Works

```text
You Explain
      ↓
AI Asks Questions
      ↓
Challenges Logic
      ↓
Finds Knowledge Gaps
      ↓
Evaluates Understanding
      ↓
Generates Learning Report
```

Curio doesn't simply provide answers.

It encourages deeper understanding by asking:

- Why?
- How does this work?
- What are the edge cases?
- Can you provide an example?
- What if this assumption changes?

---

# ✨ Features

## 🎓 Role-Reversal Learning

You become the teacher.

The AI becomes the student.

---

## ❓ Socratic Questioning

The AI asks thoughtful follow-up questions to test understanding.

Examples:

- "Why is this true?"
- "Can you explain it differently?"
- "What happens in this scenario?"

---

## 🔍 Knowledge Gap Detection

Curio identifies:

- Missing explanations
- Weak reasoning
- Incomplete understanding
- Misconceptions

---

## 📊 Understanding Evaluation

Measure learning through:

- Explanation quality
- Concept coverage
- Logical consistency
- Example usage

---

## 📄 Personalized Learning Reports

Receive reports containing:

- Strengths
- Weak areas
- Suggested improvements
- Learning score

---

## 🔌 Provider-Agnostic AI

Curio supports multiple AI providers through an abstraction layer.

This makes it easy to switch between models without changing application logic.

---

# 🏗️ Architecture

```text
┌──────────────┐
│    Client    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Routes    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Services   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ AI Provider  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Response   │
└──────────────┘
```

---

# 📂 Project Structure

```bash
src/
│
├── routes/
│   ├── health
│   ├── session
│   ├── chat
│   ├── evaluate
│   └── report
│
├── services/
│   ├── AIClient
│   ├── SessionManager
│   ├── Evaluator
│   └── ReportGenerator
│
├── models/
│
├── config/
│
├── utils/
│
└── types/
```

---

# 🔧 Core Components

## AIClient

Provides a unified interface for multiple AI providers.

---

## Session Store

Maintains:

- Conversation history
- Learning progress
- Session state

---

## Evaluation Engine

Analyzes:

- Depth of understanding
- Correctness
- Completeness

---

## Report Generator

Creates detailed learning reports for each session.

---

# 🌐 API Endpoints

## Health Check

```http
GET /health
```

---

## Create Session

```http
POST /api/session/create
```

---

## Get Session

```http
GET /api/session/{id}
```

---

## Chat with Curio

```http
POST /api/chat
```

---

## Evaluate Understanding

```http
POST /api/evaluate
```

---

## Generate Report

```http
POST /api/report
```

---

# ⚡ Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/curio.git
cd curio
```

## Install Dependencies

```bash
npm install
```

## Configure Environment

Create:

```bash
.env
```

Example:

```env
AI_PROVIDER=your_provider
API_KEY=your_api_key
```

## Run Development Server

```bash
npm run dev
```

---

# 🛠 Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS

### Backend

- Next.js API Routes
- TypeScript

### AI Layer

- Provider Abstraction Interface
- Pluggable Models

---

# 🎯 Learning Philosophy

Curio is built on two powerful educational ideas:

### 📚 Feynman Technique

> "If you can't explain it simply, you don't understand it well enough."

### 🧑‍🏫 Protégé Effect

People learn better when they teach others.

Curio combines both principles to create an active learning experience.

---

# 🗺️ Roadmap

- [ ] Multi-topic learning sessions
- [ ] Adaptive questioning
- [ ] Visual learning analytics
- [ ] Memory-based tutoring
- [ ] Collaborative learning
- [ ] Gamification
- [ ] Voice interactions

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to improve Curio, feel free to open issues or submit pull requests.

---

# 📜 License

This project is licensed under the MIT License.

---

<div align="center">

### Teach it once. Understand forever.

⭐ If you find Curio useful, consider giving it a star.

</div>