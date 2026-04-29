# Curio AI - Role-Reversal Learning Cognitive System

## System Overview

Curio AI has been transformed into a **fully dynamic, adaptive cognitive learning platform** where users teach AI and the system intelligently challenges, supports, and evaluates their understanding.

### Core Philosophy

**Users don't learn from AI. Users learn by teaching AI.** The system:
- Listens to user explanations
- Asks progressively harder questions
- Switches modes based on user performance
- Generates topic-specific mistakes for mastery validation
- Provides confidence-based session recommendations
- Generates detailed gap analysis reports

---

## Architecture

### Multi-Mode System

#### 1. **STUDENT MODE** (Default)
- AI acts as a curious, engaged student learning from the user
- Asks questions to deepen understanding
- Employs Feynman Technique principles
- Progresses through 3 difficulty levels automatically

**Difficulty Levels:**
- **Level 1 (Beginner)**: Simple, confidence-building questions
- **Level 2 (Intermediate)**: Analytical "why" questions, real-world application
- **Level 3 (Expert)**: Skeptical challenges, edge cases, deep logical attacks

**Automatic Progression:**
- User performance is scored continuously (0-1 scale)
- Progresses when average score ≥ 0.75 at Level 1, ≥ 0.80 at Level 2
- Regresses if performance drops below 0.45
- Maintains conversational continuity throughout

#### 2. **TEACHER MODE** (Triggered on Struggle)
- Triggered when user appears stuck (response quality < 0.35)
- AI becomes educator providing brief clarifications
- Minimal explanation - helps rebuild understanding independently
- Returns to Student Mode after clarification

#### 3. **RESCUE MODE** (Triggered on Partial Struggle)
- Triggered when user is partially stuck (response quality 0.35-0.50)
- AI provides subtle hints without giving answers
- Encourages independent reasoning
- Preserves user confidence

#### 4. **EVALUATOR MODE** (Session End)
- Comprehensive session analysis
- Detailed gap report generation
- Strength and weakness identification
- Personalized learning recommendations
- Mastery level assessment

---

## Key Features

### 1. **Dynamic Mistake Injection**

Instead of hardcoded mistakes, the system generates **topic-agnostic, LLM-driven mistakes**:

```
User teaches: "Quantum superposition is when a particle exists in multiple states"
AI might inject: "So superposition means particles are simultaneously in all possible states, right?"
(Subtle misconception - triggers user to defend/refine understanding)
```

**Requirements:**
- Must be hard to detect
- Must be solvable by user
- Must be specific to user's explanation
- Generated live, not from predefined lists

### 2. **Adaptive Difficulty Progression**

The system automatically analyzes each user response:
- Checks response length, reasoning indicators, examples
- Scores quality (0-1 scale)
- Tracks rolling average performance
- Progresses/regresses difficulty based on performance pattern
- Maintains min 2 successful responses per level before progression

### 3. **Confidence-Based Termination**

When system confidence reaches 75%+:
```
"Your understanding seems strong (82%)! 
Would you like to continue with harder challenges or end the session?"
```

User maintains full control while getting intelligent suggestions.

### 4. **Comprehensive Gap Analysis**

At session end, detailed report includes:
- Understanding score (0-100%)
- Mastery level (Beginner → Developing → Proficient → Mastery)
- Strengths identified
- Learning gaps by priority (High/Medium/Low)
- Misconceptions detected
- Personalized learning roadmap
- Recommended practice exercises

---

## Topic-Agnostic Architecture

### No Predefined Topics
- System works with **ANY topic** selected by user
- No hardcoded question banks
- All prompts are dynamically generated based on user input

### Dynamic Understanding Modeling
```python
# System learns what user understands about topic
user_topic_understanding = "AI learns user's mental model as they teach"

# All subsequent interactions adapt to this model:
mistake_injection()      # Generates mistakes from user's explanation
question_progression()   # Asks questions targeting their understanding level
evaluation()            # Analyzes understanding against what user taught
```

---

## Session Flow

```
1. User creates session with topic of choice
2. User explains the concept
3. AI enters STUDENT MODE at Level 1
   ├─ Asks beginner-level questions
   └─ Analyzes response quality
4. AI adapts:
   ├─ Progress to harder level if performing well
   ├─ Switch to TEACHER MODE if stuck
   ├─ Switch to RESCUE MODE if partially stuck
   ├─ Inject mistakes (~15% of responses for mastery validation)
   └─ Continue until user ends or confidence is very high
5. AI offers: "Continue or end session?"
6. On session end → EVALUATOR MODE
   ├─ Full session analysis
   ├─ Gap detection
   ├─ Learning roadmap generation
   └─ Return comprehensive report
```

---

## Response Structure

### Standard Chat Response

```json
{
  "success": true,
  "data": {
    "session_id": "sess_123...",
    "ai_message": "So if X happens, then Y would...?",
    "mode": "student",
    "difficulty_level": 2,
    "confidence_score": 65.4,
    "progress_state": {
      "question_count": 8,
      "avg_response_quality": 0.72,
      "topic": "Binary Search Trees"
    },
    "termination_offer": null
  }
}
```

### With Termination Offer

```json
{
  "success": true,
  "data": {
    "...": "...",
    "difficulty_level": 3,
    "confidence_score": 78.5,
    "termination_offer": {
      "suggested": true,
      "message": "Your understanding seems strong (79%)! Would you like to continue with harder challenges or end the session?"
    }
  }
}
```

### Evaluation Response

```json
{
  "success": true,
  "data": {
    "evaluation": {
      "overall_understanding_score": 78,
      "mastery_level": "Proficient",
      "confidence_level": 78.5,
      "strengths": [
        "Clear conceptual understanding demonstrated",
        "Can apply concepts practically"
      ],
      "gaps": [
        {
          "area": "Edge cases and special scenarios",
          "issue": "Limited exploration of boundary conditions",
          "priority": "high"
        }
      ],
      "misconceptions": [...],
      "recommendations": [...]
    },
    "report": {
      "gap_analysis": { ... },
      "learning_roadmap": [ ... ],
      "personalized_recommendations": [ ... ]
    }
  }
}
```

---

## Backend Components

### 1. **AdaptiveCognitiveController** (`ai_logic.py`)
- Main engine managing mode switching
- Analyzes user responses for quality
- Generates adaptive responses
- Handles difficulty progression
- Coordinates mistake injection

### 2. **DifficultyProgressionEngine** (`difficulty_engine.py`)
- Analyzes response quality (0-1 scale)
- Tracks performance averages
- Determines progression/regression
- Manages level transitions

### 3. **SessionEvaluator** (`evaluator.py`)
- LLM-driven session analysis
- Detects strengths, gaps, misconceptions
- Calculates understanding scores
- Generates detailed feedback

### 4. **ReportGenerator** (`report_generator.py`)
- Creates comprehensive gap reports
- Builds learning roadmaps
- Generates personalized recommendations
- Provides quick feedback summaries

### 5. **DynamicPromptBuilder** (`prompt_builder.py`)
- Generates context-aware prompts for all modes
- Supports all difficulty levels
- Maintains conversational continuity
- Topic-agnostic design

### 6. **LLMClient** (`llm_client.py`)
- Manages all Groq API interactions
- Supports structured and unstructured responses
- Handles system + user prompts
- Provides fallback mechanisms

### 7. **DynamicMistakeInjector** (`mistake_injection.py`)
- Generates LLM-driven mistakes
- Topic-specific and adaptive
- Fallback generation for robustness
- Mastery validation through mistakes

---

## State Management

### SessionState Tracking

```python
{
  # Cognitive state
  "current_mode": "student",           # or teacher, rescue, evaluator
  "difficulty_level": 2,               # 1=beginner, 2=intermediate, 3=expert
  "user_understanding_score": 72.5,    # 0-100
  "confidence_score": 68.3,            # System's confidence
  
  # Progress tracking
  "question_count": 12,
  "user_response_quality_scores": [0.65, 0.72, 0.68, ...],
  
  # History tracking
  "mode_switch_history": [
    {"timestamp": "...", "from_mode": "student", "to_mode": "teacher", "reason": "..."},
  ],
  
  # Understanding model
  "user_topic_understanding": "User understands BST insertion and deletion...",
}
```

---

## API Endpoints

### POST /chat
Create session and engage in conversation with adaptive AI.

**Request:**
```json
{
  "session_id": "sess_123...",
  "user_message": "Binary search trees are...",
  "context": null,
  "mode": "teach"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "session_id": "sess_123...",
    "ai_message": "Great! So when you insert a new node...",
    "mode": "student",
    "difficulty_level": 2,
    "confidence_score": 68.3,
    "progress_state": {...},
    "termination_offer": null
  }
}
```

### POST /evaluate
Evaluate session and generate gap report.

**Request:**
```json
{
  "session_id": "sess_123..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "evaluation": {
      "overall_understanding_score": 78,
      "mastery_level": "Proficient",
      "strengths": [...],
      "gaps": [...],
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

## Configuration & Thresholds

```python
# Confidence & Mode Switching
HIGH_CONFIDENCE_THRESHOLD = 75.0        # Offer termination at this %
TEACHER_MODE_TRIGGER = 0.35             # Response quality threshold
RESCUE_MODE_TRIGGER = 0.50              # Response quality threshold
MISTAKE_INJECTION_PROBABILITY = 0.15    # 15% chance per turn

# Difficulty Progression
PROGRESS_TO_INTERMEDIATE = 0.75         # Performance needed
PROGRESS_TO_EXPERT = 0.80
REGRESS_THRESHOLD = 0.45
MIN_RESPONSES_AT_LEVEL = 2              # Before progression
```

---

## Example Conversation Flow

**User Message 1:** "Binary search trees are data structures that organize data hierarchically..."

**AI (Level 1 Student Mode):**
```
"That's interesting! So when you add a new number to the tree, 
how does it know where to go?"
```

**User Message 2:** "It compares with the root and goes left if smaller, right if larger..."

**Quality Score:** 0.78 | **Mode:** Student | **Difficulty:** 1

**AI (Level 2 Student Mode - Progressed):**
```
"Good! But what if you need to find a specific number quickly? 
Why is a BST better than just searching through a list?"
```

**User Message 3:** "Uh... because... it's organized?"

**Quality Score:** 0.40 | **Mode:** Switched to TEACHER | **Difficulty:** 2

**AI (Teacher Mode - Clarification):**
```
"You're on the right track! The key is that each comparison eliminates 
half the remaining possibilities. Think about looking up a name in a phone book - 
you don't start at A, right?"
```

**User Message 4:** "Oh! So you eliminate half each time, that's why it's fast!"

**Quality Score:** 0.85 | **Mode:** Back to STUDENT | **Difficulty:** 3

**AI (Level 3 Expert Mode - Skeptical):**
```
"Interesting! But what if all the numbers are in order? 
1, 2, 3, 4, 5... Would that still be fast?"
```

*[Session continues with adaptive questions...]*

**At Session End → EVALUATOR MODE:**
```
Mastery Level: PROFICIENT (78%)
Strengths:
  - Understands basic BST structure
  - Grasps logarithmic advantage
  
Gaps:
  - Lacks understanding of tree imbalance (High Priority)
  - Missing knowledge of self-balancing strategies (Medium Priority)
  
Recommendations:
  1. Study AVL trees and rotations
  2. Practice insertion with pre-ordered sequences
  3. Learn about red-black trees
```

---

## For Developers

### Adding New Modes

1. Create mode-specific prompt builder in `prompt_builder.py`
2. Add mode logic to `AdaptiveCognitiveController`
3. Update session state tracking
4. Add mode to SessionState Literal types

### Customizing Difficulty

Edit thresholds in `DifficultyProgressionEngine`:
```python
PROGRESS_TO_INTERMEDIATE_THRESHOLD = 0.75  # Adjust difficulty curve
REGRESS_THRESHOLD = 0.45
```

### Fine-tuning Response Analysis

Adjust scoring weights in `analyze_response_quality()`:
```python
# Currently: length=0.2, reasoning=0.15, examples=0.15, etc.
# Customize for your use case
```

---

## Limitations & Future Enhancements

### Current Limitations
- Mistake injection may occasionally miss topic-specific nuances
- LLM response quality depends on Groq API availability
- Gap detection is pattern-based (can be enhanced with more data)

### Future Enhancements
- Cross-session learning tracking (spaced repetition)
- Peer comparison metrics
- Topic relationships and prerequisite mapping
- Custom evaluation rubrics
- Adaptive pacing based on user engagement
- Multi-language support

---

## Quick Start

### 1. Create Session
```bash
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "topic": "Quantum Entanglement"}'
```

### 2. Start Teaching
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc...",
    "user_message": "Quantum entanglement is when two particles are connected...",
    "mode": "teach"
  }'
```

### 3. Continue Conversation
(AI will ask follow-up questions adaptively)

### 4. End & Evaluate
```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess_abc..."}'
```

---

## System Characteristics

✅ **Fully Dynamic** - Works with ANY topic selected by user  
✅ **Adaptive** - Difficulty and mode adjust in real-time based on performance  
✅ **Intelligent** - LLM-driven analysis and response generation  
✅ **Supportive** - Switches to teaching/rescue when user struggles  
✅ **Challenging** - Progressively harder questions and mistake injection  
✅ **Comprehensive** - Detailed gap analysis and learning roadmaps  
✅ **User-Controlled** - Users decide when to end, with smart suggestions  
✅ **Scalable** - Modular architecture ready for expansion  

---

## Success Metrics

A successful Curio session:
- User remains engaged throughout
- AI difficulty matches user capability
- Misconceptions are identified and corrected
- User reaches proficiency or mastery
- User leaves with clear learning next steps
- System confidence correlates with actual understanding

---

**Curio AI: Where Teaching Is Learning**
