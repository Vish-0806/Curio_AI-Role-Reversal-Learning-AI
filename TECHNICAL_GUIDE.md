# Curio AI Backend - Technical Implementation Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Web/Mobile)                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Routes Layer                         │
│  /session  /chat  /evaluate  /report  /health               │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            Application Service Layer                          │
│  ├─ ai_service.py (Main AI interface)                       │
│  ├─ session_manager.py (State management)                   │
│  ├─ input_processor.py (Request processing)                 │
│  └─ report_generator.py (Report generation)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│         Adaptive Cognitive Engine (ai_engine/)               │
│  ├─ ai_logic.py                                              │
│  │  └─ AdaptiveCognitiveController                          │
│  │     ├─ analyze_user_response()                           │
│  │     ├─ generate_adaptive_response()                      │
│  │     └─ generate_session_evaluation()                     │
│  │                                                           │
│  ├─ difficulty_engine.py                                    │
│  │  └─ DifficultyProgressionEngine                          │
│  │     ├─ analyze_response_quality()                        │
│  │     ├─ should_progress_difficulty()                      │
│  │     └─ get_next_difficulty_level()                       │
│  │                                                           │
│  ├─ prompt_builder.py                                       │
│  │  ├─ build_student_mode_prompt()                          │
│  │  ├─ build_teacher_mode_prompt()                          │
│  │  ├─ build_rescue_mode_prompt()                           │
│  │  └─ build_evaluator_mode_prompt()                        │
│  │                                                           │
│  ├─ mistake_injection.py                                    │
│  │  └─ inject_mistake_llm()                                 │
│  │     (Dynamic, topic-agnostic mistake generation)         │
│  │                                                           │
│  ├─ evaluator.py                                            │
│  │  └─ SessionEvaluator                                     │
│  │     ├─ evaluate_session()                                │
│  │     ├─ evaluate_response()                               │
│  │     └─ _parse_gaps()                                     │
│  │                                                           │
│  └─ llm_client.py                                           │
│     ├─ call_llm()                                            │
│     ├─ call_llm_structured()                                │
│     └─ call_llm_with_system_prompt()                        │
│                                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            External Services & Storage                        │
│  ├─ Groq API (llama-3.1-8b-instant)                         │
│  ├─ MongoDB (Session persistence)                           │
│  └─ Environment Variables (.env)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py (FastAPI app initialization)
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py (Configuration constants)
│   │   └── settings.py (Environment-based settings)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── session_model.py ✅ UPDATED (Cognitive tracking)
│   │   ├── chat_model.py ✅ UPDATED (New response fields)
│   │   ├── evaluation_model.py
│   │   └── report_model.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py ✅ UPDATED (Uses adaptive controller)
│   │   ├── evaluate.py ✅ UPDATED (LLM-driven evaluation)
│   │   ├── session.py (Session lifecycle)
│   │   └── report.py (Report delivery)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py ✅ UPDATED (New interface)
│   │   ├── session_manager.py (Session state persistence)
│   │   ├── input_processor.py (Input validation)
│   │   ├── report_generator.py ✅ UPDATED (Gap reports)
│   │   │
│   │   └── ai_engine/
│   │       ├── __init__.py
│   │       ├── ai_logic.py ✅ NEW (AdaptiveCognitiveController)
│   │       ├── difficulty_engine.py ✅ NEW (Progression logic)
│   │       ├── prompt_builder.py ✅ UPDATED (All modes + difficulty)
│   │       ├── mistake_injection.py ✅ UPDATED (LLM-driven)
│   │       ├── evaluator.py ✅ UPDATED (Comprehensive evaluation)
│   │       ├── llm_client.py ✅ UPDATED (Structured responses)
│   │       └── prompts/
│   │           └── student_prompt.txt (Legacy - now dynamic)
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── mongodb.py (MongoDB connection)
│   │   └── testdb.py (In-memory fallback)
│   │
│   └── utils/
│       ├── __init__.py
│       ├── error_handler.py
│       ├── helpers.py
│       └── logger.py
│
├── check_app.py (Health check script)
├── main.py (Entry point)
├── requirements.txt
├── run.bat (Windows launcher)
└── dump_error.bat (Error logging)
```

---

## Data Flow Examples

### Chat Flow (with Mode Switching)

```
User Input
    ↓
[Input Processor] → Clean & validate
    ↓
[Session Manager] → Load session state, track conversation
    ↓
[Adaptive Cognitive Controller]
    ├─ analyze_user_response() → Quality score (0-1)
    ├─ Check mode triggers:
    │  ├─ If quality < 0.35 → Switch to TEACHER MODE
    │  ├─ Else if quality < 0.50 → Switch to RESCUE MODE
    │  └─ Else → Stay in STUDENT MODE
    ├─ Update session tracking (scores, question count, confidence)
    └─ Check difficulty progression:
       ├─ Calculate average performance
       ├─ Determine if should progress/regress
       └─ Update difficulty_level
    ↓
[Prompt Builder] → Generate mode-specific, difficulty-aware prompt
    ├─ System: "You are a curious student..."
    ├─ Context: Conversation history
    └─ User: User's latest explanation
    ↓
[LLM Client] → Call Groq API
    ├─ 85% chance: Generate question (Student/Teacher/Rescue mode)
    └─ 15% chance: Generate mistake injection (mastery validation)
    ↓
[Response Formatter]
    ├─ ai_message (LLM output)
    ├─ mode (current AI mode)
    ├─ difficulty_level (current progression level)
    ├─ confidence_score (0-100)
    ├─ progress_state (session metrics)
    └─ termination_offer (if confidence > 75%)
    ↓
[Session Manager] → Store AI turn with annotations
    ↓
Return Response to Frontend
```

### Evaluation Flow (Session End)

```
Evaluation Request
    ↓
[Session Manager] → Load full session state
    ↓
[SessionEvaluator]
    ├─ Build conversation text for LLM
    ├─ Call LLM with analysis prompt
    ├─ Parse LLM output for:
    │  ├─ Strengths identified
    │  ├─ Learning gaps
    │  ├─ Misconceptions
    │  └─ Overall understanding score
    └─ Assess mastery level:
       ├─ 85%+ → Mastery
       ├─ 70-85% → Proficient
       ├─ 50-70% → Developing
       └─ <50% → Beginner
    ↓
[Report Generator]
    ├─ Build comprehensive summary
    ├─ Analyze gaps by priority
    ├─ Explain gap importance
    ├─ Suggest remediation strategies
    └─ Create multi-step learning roadmap
    ↓
[Session Manager] → Store evaluation result
    ↓
Return Evaluation + Report to Frontend
```

---

## Mode Switching Decision Tree

```
User Response Quality Score (0-1)
│
├─ < 0.35 (Very Weak)
│  └─ → TEACHER MODE
│     (Provide brief clarification)
│     └─ After clarification → Resume STUDENT MODE
│
├─ 0.35-0.50 (Weak)
│  └─ → RESCUE MODE
│     (Provide hints without answers)
│     └─ After hints → Resume STUDENT MODE
│
├─ 0.50-0.75 (Moderate)
│  └─ → STUDENT MODE (Continue)
│     (Ask follow-up questions)
│
└─ > 0.75 (Strong)
   └─ → STUDENT MODE (Prepare progression)
      (At Level 1-2: Progress to next difficulty)
      (At Level 3: Check confidence)
      (If confidence > 75%: Offer termination)
```

---

## Difficulty Progression Algorithm

```
Performance Tracking:
  - Maintain list of recent response quality scores
  - Calculate rolling average (last 5 responses)
  - Track consecutive responses at current level

Progression Decision:
  IF current_level == 1:
    IF avg_performance >= 0.75 AND responses_at_level >= 2:
      → Progress to Level 2
      → Reset level counter
    ELSE:
      → Stay at Level 1
  
  ELSE IF current_level == 2:
    IF avg_performance >= 0.80 AND responses_at_level >= 2:
      → Progress to Level 3
      → Reset level counter
    ELSE IF avg_performance < 0.45:
      → Regress to Level 1
    ELSE:
      → Stay at Level 2
  
  ELSE IF current_level == 3:
    IF avg_performance < 0.45:
      → Regress to Level 2
      → Reset level counter
    ELSE:
      → Stay at Level 3

Progression Triggers & Thresholds:
  PROGRESS_TO_INTERMEDIATE_THRESHOLD = 0.75
  PROGRESS_TO_EXPERT_THRESHOLD = 0.80
  REGRESS_THRESHOLD = 0.45
  MIN_RESPONSES_AT_LEVEL = 2
```

---

## Response Quality Scoring

```python
def analyze_response_quality(response_text: str, difficulty_level: int) -> float:
    score = 0.5  # Baseline
    
    # Length scoring
    word_count = len(response_text.split())
    if word_count < 10:
        score -= 0.15  # Too brief
    elif word_count > 50:
        score += 0.15  # Excellent detail
    
    # Reasoning indicators
    if any(word in response for word in ["because", "therefore", "since"]):
        score += 0.15
    
    # Examples
    if any(word in response for word in ["example", "like", "such as"]):
        score += 0.15
    
    # Nuance (Level 2+)
    if difficulty_level >= 2:
        if any(word in response for word in ["however", "but", "depends"]):
            score += 0.1
    
    # Edge cases (Level 3)
    if difficulty_level >= 3:
        if any(word in response for word in ["edge case", "boundary", "exception"]):
            score += 0.1
    
    # Penalty for uncertainty at higher levels
    if difficulty_level >= 2:
        if any(word in response for word in ["i don't know", "not sure"]):
            score -= 0.2
    
    return max(0.0, min(1.0, score))
```

---

## LLM Integration Points

### 1. Question Generation (Student Mode)
```
System: "You are a curious student learning about [TOPIC]..."
User: [user's explanation]
→ LLM generates follow-up question at [DIFFICULTY] level
```

### 2. Clarification (Teacher Mode)
```
System: "You are a patient teacher helping clarify [TOPIC]..."
User: [user's confusion point]
→ LLM generates minimal, focused explanation
```

### 3. Hints (Rescue Mode)
```
System: "You are a rescue guide providing hints..."
User: [user's struggle]
→ LLM generates leading question without full answer
```

### 4. Mistake Injection
```
System: "Generate a subtle misconception about [TOPIC]..."
Context: [user's explanations]
→ LLM generates topic-specific, hard-to-detect mistake
```

### 5. Evaluation & Gap Analysis
```
System: "You are a cognitive learning evaluator..."
Context: [full conversation]
→ LLM analyzes strengths, gaps, misconceptions
```

---

## Environment Configuration

### Required Environment Variables (.env)
```bash
# LLM Configuration
GROQ_API_KEY=<your_groq_api_key>

# Database Configuration  
MONGODB_URI=<mongodb_connection_string>
MONGODB_DB_NAME=curio_ai

# Server Configuration
PORT=8000
HOST=127.0.0.1
DEBUG=False

# Session Configuration
SESSION_TTL_MINUTES=120  # Session timeout
```

### Settings Resolution Order
1. Environment variables (.env file)
2. config/settings.py defaults
3. Fallback in-memory storage (if MongoDB unavailable)

---

## Testing the System

### 1. Test Session Creation
```bash
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "topic": "Recursion"}'

# Expected response:
{
  "success": true,
  "data": {
    "session_id": "sess_...",
    "created_at": "2024-04-30T...",
    "expires_at": "2024-04-30T..."
  }
}
```

### 2. Test Chat (Initial Teaching)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_...",
    "user_message": "Recursion is when a function calls itself to solve smaller versions of the same problem",
    "mode": "teach"
  }'

# Expected response:
{
  "success": true,
  "data": {
    "session_id": "sess_...",
    "ai_message": "Great explanation! So when a function calls itself...",
    "mode": "student",
    "difficulty_level": 1,
    "confidence_score": 45.5,
    "progress_state": {
      "question_count": 1,
      "avg_response_quality": 0.75,
      "topic": "Recursion"
    }
  }
}
```

### 3. Test Mode Switching (Weak Response)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_...",
    "user_message": "Um... I'm not sure"
  }'

# Expected response:
{
  "success": true,
  "data": {
    "mode": "teacher",  # ← Switched to teacher mode
    "ai_message": "No worries! Think about a simple example...",
    "difficulty_level": 1,
    "confidence_score": 32.1
  }
}
```

### 4. Test Difficulty Progression (Strong Responses)
```bash
# After 2+ strong responses at Level 1
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{...}'

# Expected response:
{
  "success": true,
  "data": {
    "mode": "student",
    "difficulty_level": 2,  # ← Progressed to intermediate
    "ai_message": "So why do you think recursion is better than loops in some cases?",
    "confidence_score": 62.3
  }
}
```

### 5. Test Evaluation
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess_..."}'

# Expected response:
{
  "success": true,
  "data": {
    "evaluation": {
      "overall_understanding_score": 72,
      "mastery_level": "Developing",
      "confidence_level": 68.3,
      "strengths": ["Grasps core recursion concept"],
      "gaps": [{"area": "Base case handling", "priority": "high"}],
      "recommendations": [...]
    },
    "report": {
      "gap_analysis": {...},
      "learning_roadmap": [...]
    }
  }
}
```

---

## Debugging & Monitoring

### Logging Levels
- **DEBUG**: Detailed flow and intermediate results
- **INFO**: Major operations (session created, evaluated, etc.)
- **WARNING**: Potential issues (MongoDB unavailable, etc.)
- **ERROR**: Failed operations
- **EXCEPTION**: Unexpected errors with full traceback

### Key Logs to Monitor
```
[DEBUG] Chat request received
[DEBUG] Session retrieved: session_id=..., conversation_length=...
[DEBUG] AI response generated: mode=..., difficulty=...
[INFO] Chat turn completed successfully
[ERROR] Error generating AI response: error=...
```

### Health Check Endpoint
```bash
curl http://localhost:8000/health

# Expected response:
{
  "status": "ok",
  "services": {
    "database": "connected",
    "llm": "available",
    "sessions": 3
  }
}
```

---

## Performance Optimization

### Caching Strategies
- Cache recent prompts to reduce LLM calls
- Store frequently asked question patterns
- Memoize response quality calculations

### Request Optimization
- Batch multiple turns if needed
- Compress large conversation histories
- Archive completed sessions

### Database Optimization
- Index on session_id, user_id, created_at
- TTL index on expires_at for auto-cleanup
- Archive old sessions to separate collection

---

## Scaling Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Session manager handles concurrent requests
- Database becomes bottleneck - scale MongoDB

### Vertical Scaling
- Increase LLM token limits for longer contexts
- Optimize difficulty engine calculations
- Cache more aggressive

### Cost Optimization
- Batch evaluations during off-peak hours
- Use cheaper LLM models for simple tasks
- Implement response caching

---

## Troubleshooting

### Issue: "Error generating response"
**Cause:** LLM API call failed  
**Solution:** 
- Check GROQ_API_KEY environment variable
- Verify Groq API is accessible
- Check request rate limits

### Issue: MongoDB connection fails
**Cause:** Database unreachable  
**Solution:**
- Check MONGODB_URI connection string
- Verify MongoDB instance is running
- Check firewall rules for port 27017

### Issue: Difficulty not progressing
**Cause:** Threshold settings too high  
**Solution:**
- Check response quality scores in logs
- Adjust thresholds in DifficultyProgressionEngine
- Verify MIN_RESPONSES_AT_LEVEL is being met

### Issue: Modes not switching
**Cause:** Quality score thresholds misconfigured  
**Solution:**
- Monitor response quality scores
- Verify TEACHER_MODE_TRIGGER and RESCUE_MODE_TRIGGER
- Check mode switching logic in adaptive controller

---

## Deployment Checklist

- [ ] Set GROQ_API_KEY environment variable
- [ ] Configure MongoDB connection string
- [ ] Set SESSION_TTL_MINUTES (recommended: 120)
- [ ] Enable DEBUG=False for production
- [ ] Configure logging levels (INFO for production)
- [ ] Set up error monitoring/alerting
- [ ] Test all endpoints before deploying
- [ ] Verify LLM quality on sample topics
- [ ] Load test with concurrent users
- [ ] Set up database backups
- [ ] Configure rate limiting if needed
- [ ] Document any customized thresholds

---

## Future Architecture Improvements

1. **Vector Database Integration** - Semantic search for similar sessions
2. **Caching Layer** - Redis for prompt/response caching
3. **Message Queue** - Async evaluation for long sessions
4. **Analytics Dashboard** - Track learning patterns across users
5. **Custom Model Fine-tuning** - Domain-specific model optimization
6. **Multi-LLM Support** - Fallback to alternative providers
