# Curio AI - File Reference Guide

## Core System Files

### Main Engine
- **ai_logic.py** - AdaptiveCognitiveController (main brain)
  - `generate_adaptive_response()` - Main entry point
  - `analyze_user_response()` - Quality scoring
  - `generate_session_evaluation()` - Evaluation generation
  
- **difficulty_engine.py** - DifficultyProgressionEngine (NEW)
  - `analyze_response_quality()` - Score responses 0-1
  - `should_progress_difficulty()` - Check progression ready
  - `get_next_difficulty_level()` - Determine new level

- **prompt_builder.py** - Dynamic Prompt Generation
  - `build_student_mode_prompt()` - Student questions
  - `build_teacher_mode_prompt()` - Teaching clarifications
  - `build_rescue_mode_prompt()` - Rescue hints
  - `build_evaluator_mode_prompt()` - Evaluation analysis

### Specialized Services
- **mistake_injection.py** - Dynamic Mistake Generation (UPDATED)
  - `inject_mistake_llm()` - LLM-driven mistakes
  - `generate_mistake_injection_prompt()` - Prompt building
  - `generate_fallback_mistake()` - Intelligent fallback

- **evaluator.py** - Comprehensive Evaluation (UPDATED)
  - `SessionEvaluator.evaluate_session()` - Full evaluation
  - `SessionEvaluator.evaluate_response()` - Single response
  - `_parse_gaps()` - Extract learning gaps
  - `_parse_misconceptions()` - Detect misconceptions

- **llm_client.py** - LLM Integration (UPDATED)
  - `call_llm()` - Basic LLM calls
  - `call_llm_structured()` - Structured responses
  - `call_llm_with_system_prompt()` - System+user prompts

### Application Layer
- **ai_service.py** - Main AI Interface (UPDATED)
  - `get_ai_response()` - Adaptive response generation
  - `evaluate_user_response()` - Single response evaluation
  - `generate_session_evaluation()` - Session evaluation

- **report_generator.py** - Report Generation (UPDATED)
  - `generate_report()` - Comprehensive report
  - `_build_gap_analysis_report()` - Gap analysis
  - `_build_learning_roadmap()` - Learning paths

- **session_manager.py** - Session Persistence
  - `create_session()` - Create new session
  - `get_session()` - Load session
  - `append_turn()` - Add conversation turn
  - `update_last_evaluation()` - Store evaluation

### Routes
- **chat.py** - Chat Endpoint (UPDATED)
  - `POST /chat` - User message handling
  
- **evaluate.py** - Evaluation Endpoint (UPDATED)
  - `POST /evaluate` - Session evaluation

### Data Models
- **session_model.py** - Session State (UPDATED)
  - `SessionState` - Full session with cognitive tracking
  - `ConversationTurn` - Individual message turn

- **chat_model.py** - Chat Models (UPDATED)
  - `ChatRequest` - Request schema
  - `ChatResponse` - Response schema with cognitive fields

---

## Configuration & Constants
- **config/settings.py** - Environment-based settings
- **config/constants.py** - System constants

---

## Utility Files
- **utils/logger.py** - Logging
- **utils/error_handler.py** - Error handling
- **utils/helpers.py** - Helper functions
- **database/mongodb.py** - MongoDB connection

---

## Documentation Files

### System Documentation
1. **COGNITIVE_SYSTEM.md** - Feature documentation
   - 20+ pages
   - Multi-mode system details
   - Architecture overview
   - Example conversations
   - API reference
   - Configuration guide

2. **TECHNICAL_GUIDE.md** - Implementation guide
   - 25+ pages
   - System architecture
   - Data flow examples
   - Decision trees
   - Algorithms
   - Debugging guide
   - Deployment checklist

3. **IMPLEMENTATION_SUMMARY.md** - Build summary
   - 15+ pages
   - What was built
   - Component descriptions
   - File structure
   - Response examples

4. **QUICK_START.md** - Getting started
   - 10+ pages
   - Setup instructions
   - Example conversation
   - Feature testing
   - Troubleshooting

5. **PROJECT_COMPLETION.md** - Project summary
   - Requirements checklist
   - Architecture overview
   - Feature highlights
   - Success metrics

6. **This File** - File reference guide

---

## Testing the System

### Quick Tests
1. **Health Check**
   - GET /health

2. **Session Creation**
   - POST /session
   - Body: {"user_id": "test", "topic": "Recursion"}

3. **Chat Turn**
   - POST /chat
   - Body: {"session_id": "...", "user_message": "..."}

4. **Evaluation**
   - POST /evaluate
   - Body: {"session_id": "..."}

---

## Key Configuration Variables

```python
# Thresholds
TEACHER_MODE_TRIGGER_THRESHOLD = 0.35
RESCUE_MODE_TRIGGER_THRESHOLD = 0.50
HIGH_CONFIDENCE_THRESHOLD = 75.0

# Difficulty Progression
PROGRESS_TO_INTERMEDIATE_THRESHOLD = 0.75
PROGRESS_TO_EXPERT_THRESHOLD = 0.80
REGRESS_THRESHOLD = 0.45
MIN_RESPONSES_AT_LEVEL = 2

# Mistake Injection
MISTAKE_INJECTION_PROBABILITY = 0.15
```

---

## Environment Variables Required

```
GROQ_API_KEY=<your_key>
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=curio_ai
SESSION_TTL_MINUTES=120
DEBUG=False
PORT=8000
HOST=127.0.0.1
```

---

## Data Flow Paths

### Chat Request
```
Route: POST /chat
├─ Input: ChatRequest (session_id, user_message)
├─ Process:
│  ├─ [Input Processor] Validate & clean
│  ├─ [Session Manager] Load session
│  ├─ [Adaptive Controller] Generate response
│  ├─ [Session Manager] Store turn
│  └─ [Response Formatter] Format for frontend
└─ Output: ChatResponse (JSON with cognitive metadata)
```

### Evaluation Request
```
Route: POST /evaluate
├─ Input: EvaluationRequest (session_id)
├─ Process:
│  ├─ [Session Manager] Load full session
│  ├─ [SessionEvaluator] Analyze conversation
│  ├─ [Report Generator] Build gap report
│  ├─ [Session Manager] Store evaluation
│  └─ [Response Formatter] Format report
└─ Output: EvaluationResponse (comprehensive report)
```

---

## Mode Switching Logic

```
Quality Score < 0.35
└─ Switch to TEACHER MODE
   ├─ Provide brief clarification
   └─ Return to STUDENT MODE

Quality Score 0.35-0.50
└─ Switch to RESCUE MODE
   ├─ Provide subtle hints
   └─ Return to STUDENT MODE

Quality Score > 0.50
└─ Stay in STUDENT MODE
   ├─ Ask follow-up question
   └─ Check for difficulty progression
```

---

## Difficulty Progression Logic

```
Current Level = 1:
├─ Avg Performance >= 0.75 → Progress to Level 2
└─ Else → Stay at Level 1

Current Level = 2:
├─ Avg Performance >= 0.80 → Progress to Level 3
├─ Avg Performance < 0.45 → Regress to Level 1
└─ Else → Stay at Level 2

Current Level = 3:
├─ Avg Performance < 0.45 → Regress to Level 2
└─ Else → Stay at Level 3
```

---

## Response Quality Scoring

```
Base Score: 0.5

Modifiers:
+ 0.15 if word_count > 20
- 0.15 if word_count < 10
+ 0.15 if reasoning detected (because, therefore, since)
+ 0.15 if examples detected (like, such as, example)
+ 0.10 if nuance detected (Level 2+)
+ 0.10 if edge cases detected (Level 3)
- 0.20 if uncertainty detected (Level 2+)

Result: Clamp to 0.0-1.0
```

---

## Key Classes & Methods

### AdaptiveCognitiveController
```python
class AdaptiveCognitiveController:
    def generate_adaptive_response(session, user_input, force_mode)
    def analyze_user_response(response_text, difficulty_level)
    def _assess_confidence(quality_score)
    def generate_session_evaluation(session)
    def _generate_student_mode_response(...)
    def _generate_teacher_mode_response(...)
    def _generate_rescue_mode_response(...)
```

### DifficultyProgressionEngine
```python
class DifficultyProgressionEngine:
    def analyze_response_quality(response_text, difficulty_level)
    def calculate_average_performance(recent_scores, window_size)
    def should_progress_difficulty(current_difficulty, avg_perf, responses_at_level)
    def should_regress_difficulty(current_difficulty, avg_performance)
    def get_next_difficulty_level(current_difficulty, avg_perf, responses_at_level)
    def get_difficulty_context(difficulty_level)
```

### SessionEvaluator
```python
class SessionEvaluator:
    def evaluate_session(session)
    def evaluate_response(user_input, difficulty_level)
    def _get_llm_analysis(conversation, topic)
    def _parse_strengths(analysis)
    def _parse_gaps(analysis)
    def _parse_misconceptions(analysis)
    def _calculate_understanding_score(response_scores, gap_count, strength_count)
    def _assess_mastery(understanding_score)
```

---

## Integration Points

### Frontend Integration
All responses follow `ResponseEnvelope[T]` pattern:
```json
{
  "success": true,
  "data": {...},
  "error": null,
  "request_id": "...",
  "timestamp": "..."
}
```

### LLM Integration
All LLM calls through `llm_client.py`:
- `call_llm()` - Basic calls
- `call_llm_structured()` - Structured JSON
- `call_llm_with_system_prompt()` - System+user

### Database Integration
All session persistence through `session_manager.py`:
- Create, read, update operations
- MongoDB with fallback to in-memory

---

## Debugging & Monitoring

### Key Log Points
```
[DEBUG] Chat request received
[DEBUG] Session retrieved
[DEBUG] AI response generated
[DEBUG] Input processed
[INFO] Chat turn completed successfully
[INFO] Session evaluated successfully
[ERROR] Error generating AI response
[EXCEPTION] Unexpected error with traceback
```

### Health Check Endpoint
```
GET /health
Returns: {status, services, session_count}
```

---

## Customization Points

### Adjust Difficulty Thresholds
Edit `DifficultyProgressionEngine`:
```python
PROGRESS_TO_INTERMEDIATE_THRESHOLD = 0.75  # ← Adjust
PROGRESS_TO_EXPERT_THRESHOLD = 0.80        # ← Adjust
REGRESS_THRESHOLD = 0.45                   # ← Adjust
```

### Adjust Mode Triggers
Edit `AdaptiveCognitiveController`:
```python
TEACHER_MODE_TRIGGER_THRESHOLD = 0.35      # ← Adjust
RESCUE_MODE_TRIGGER_THRESHOLD = 0.50       # ← Adjust
HIGH_CONFIDENCE_THRESHOLD = 75.0           # ← Adjust
```

### Adjust Mistake Frequency
Edit `AdaptiveCognitiveController`:
```python
MISTAKE_INJECTION_PROBABILITY = 0.15       # ← Adjust (15%)
```

### Adjust Response Scoring Weights
Edit `DifficultyProgressionEngine.analyze_response_quality()`:
```python
# Modify point allocations
```

---

## Performance Optimization Tips

1. **Cache prompts** - Store generated prompts for similar topics
2. **Batch evaluations** - Run multiple evaluations together
3. **Archive sessions** - Move old sessions to archive collection
4. **Index database** - Add indexes on session_id, user_id, created_at
5. **Compress history** - Archive old conversation turns

---

## Troubleshooting Quick Reference

| Issue | Cause | Solution |
|-------|-------|----------|
| Error generating response | LLM API fail | Check GROQ_API_KEY |
| Session not found | Wrong ID | Copy exact session_id |
| Connection failed | DB down | Check MongoDB, uses in-memory fallback |
| Difficulty not progressing | Threshold too high | Need 2+ responses at 75%+ quality |
| Modes not switching | Wrong thresholds | Verify TEACHER/RESCUE thresholds |

---

## Testing Checklist

- [ ] Create session
- [ ] Send weak response (triggers TEACHER MODE)
- [ ] Send strong responses (difficulty progresses)
- [ ] Check confidence score
- [ ] Verify termination offer at > 75%
- [ ] End session and evaluate
- [ ] Verify gap analysis in response
- [ ] Check learning roadmap generation

---

## Deployment Checklist

- [ ] Set all environment variables
- [ ] Test LLM connectivity
- [ ] Test MongoDB connectivity
- [ ] Enable ERROR+ logging for production
- [ ] Set DEBUG=False
- [ ] Configure rate limiting
- [ ] Set up monitoring/alerting
- [ ] Document any custom thresholds
- [ ] Backup database before deploying
- [ ] Test with variety of topics

---

This reference guide provides quick navigation to all system components, configuration options, and integration points.

For detailed information, see the documentation files:
- **COGNITIVE_SYSTEM.md** - Feature deep-dive
- **TECHNICAL_GUIDE.md** - Architecture details
- **QUICK_START.md** - Getting started
