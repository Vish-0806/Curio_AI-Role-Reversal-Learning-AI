# Curio AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Prerequisites
```bash
# Ensure you have:
- Python 3.9+
- MongoDB running (or it will fall back to in-memory)
- Groq API key
```

### 2. Environment Setup
```bash
# Create/update .env file in backend/
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb://localhost:27017/curio_ai
MONGODB_DB_NAME=curio_ai
SESSION_TTL_MINUTES=120
DEBUG=False
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Start the Server
```bash
# Option A: Windows
run.bat

# Option B: Manual
python -m uvicorn app.main:app --app-dir d:\CurioAI\backend --host 127.0.0.1 --port 8000
```

### 5. Test the API
```bash
# Create a session
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "topic": "Recursion"}'

# Note the session_id from response, then:

# Start teaching
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "PASTE_SESSION_ID_HERE",
    "user_message": "Recursion is when a function calls itself",
    "mode": "teach"
  }'

# Watch AI ask follow-up questions!
# Continue the conversation...
# Then evaluate at the end:

curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "PASTE_SESSION_ID_HERE"}'
```

---

## 📊 What to Watch For

### Mode Switching
As you respond:
- **Weak response** → AI switches to **TEACHER MODE** (clarifies concept)
- **Partial response** → AI switches to **RESCUE MODE** (provides hints)
- **Strong response** → AI stays in **STUDENT MODE** (asks deeper questions)

### Difficulty Progression
- First turn: Level 1 (simple questions)
- After 2+ strong responses: Level 2 (analytical questions)
- After 2+ strong responses at Level 2: Level 3 (expert-level challenges)

### Confidence Scoring
- Tracks as percentage (0-100%)
- When reaches 75%+: System offers to end session
- You control if you want to continue or end

### Evaluation
After ending session, you get:
- **Understanding Score** (0-100%)
- **Mastery Level** (Beginner → Developing → Proficient → Mastery)
- **Strengths** identified
- **Learning Gaps** by priority
- **Misconceptions** detected
- **Personalized Learning Roadmap**

---

## 🎯 Example: Teaching Binary Search

```bash
# 1. Create session
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"topic": "Binary Search"}'

# Response: session_id = "sess_abc123"

# 2. First turn: Level 1, Student Mode
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "user_message": "Binary search is an algorithm that finds an element in a sorted array by repeatedly dividing the search interval in half"
  }'

# AI Response:
# "That's a great explanation! So when you're looking for a number,
#  how do you know whether to search in the left half or right half?"
# 
# Metadata:
# - mode: "student"
# - difficulty_level: 1
# - confidence_score: 62.3

# 3. Your response
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "user_message": "You compare the target with the middle element. If it's smaller, search left; if larger, search right."
  }'

# AI Response:
# "Excellent! Now why is this better than searching every element one by one?"
# 
# Metadata:
# - mode: "student" (still)
# - difficulty_level: 1 (quality score high)
# - confidence_score: 71.2

# 4. Your response (strong answer)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "user_message": "Because each step eliminates half the remaining elements, so it's logarithmic - much faster than linear search which checks every element."
  }'

# AI Response:
# "Perfect! So if the array is in reverse order, would binary search still work?"
# 
# Metadata:
# - mode: "student"
# - difficulty_level: 2  ← PROGRESSED!
# - confidence_score: 78.5

# 5. Your response (weak)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "user_message": "Hmm... I'm not sure"
  }'

# AI Switches to TEACHER MODE:
# "No worries! Think about what binary search assumes about the array.
#  What order must it be in?"
# 
# Metadata:
# - mode: "teacher" ← MODE SWITCHED!
# - difficulty_level: 2
# - confidence_score: 45.3

# 6. Your clarified response
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "user_message": "Oh right! It has to be sorted in ascending order"
  }'

# AI Returns to STUDENT MODE with harder question:
# "Good! So what if we wanted to search a DESCENDING array efficiently?
#  What would need to change?"
# 
# Metadata:
# - mode: "student" ← BACK TO STUDENT
# - difficulty_level: 2
# - confidence_score: 68.7

# 7. End session and evaluate
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "sess_abc123"}'

# Response includes:
# {
#   "evaluation": {
#     "overall_understanding_score": 74,
#     "mastery_level": "Developing",
#     "confidence_level": 68.7,
#     "strengths": [
#       "Understands basic binary search mechanics",
#       "Grasps logarithmic advantage"
#     ],
#     "gaps": [
#       {
#         "area": "Edge cases",
#         "issue": "Didn't consider reverse sorting",
#         "priority": "high"
#       }
#     ],
#     "recommendations": [
#       "Priority: Study variations of binary search (reverse arrays, etc.)",
#       "Practice implementing binary search in code",
#       "Explore: What happens with duplicate values?"
#     ]
#   },
#   "report": {
#     "gap_analysis": {...},
#     "learning_roadmap": [
#       {
#         "step": 1,
#         "priority": "HIGH",
#         "action": "Master edge cases",
#         "timeline": "This week"
#       },
#       {
#         "step": 2,
#         "priority": "MEDIUM",
#         "action": "Implement variants",
#         "timeline": "Next week"
#       }
#     ]
#   }
# }
```

---

## 🔍 Understanding the Response

### Chat Response Breakdown
```json
{
  "session_id": "sess_...",           // Session identifier
  "ai_message": "So when...",         // The AI's actual question/response
  "mode": "student",                  // Current AI mode
  "difficulty_level": 2,              // Current difficulty (1/2/3)
  "confidence_score": 71.2,           // System's confidence (0-100%)
  "progress_state": {
    "question_count": 5,              // Total questions asked
    "avg_response_quality": 0.74,    // Your average quality (0-1)
    "topic": "Binary Search"
  },
  "termination_offer": {              // When confidence > 75%
    "suggested": true,
    "message": "Your understanding seems strong..."
  }
}
```

### Evaluation Response Breakdown
```json
{
  "evaluation": {
    "overall_understanding_score": 74,     // 0-100%
    "mastery_level": "Developing",         // Classification
    "confidence_level": 68.7,              // How sure system is
    "strengths": [                         // What you're good at
      "Understands core concept",
      "Can apply practically"
    ],
    "gaps": [                              // What to improve
      {
        "area": "Edge cases",
        "issue": "Limited exploration",
        "priority": "high",
        "why_it_matters": "Missing edge cases cause bugs",
        "suggested_focus": "Identify 5 edge cases..."
      }
    ],
    "misconceptions": [                    // Wrong ideas detected
      {
        "issue": "Assumed X always true",
        "severity": "high",
        "action": "Review and revise assumption"
      }
    ],
    "recommendations": [                   // Next steps
      "Priority: Review edge cases",
      "Study topic variations",
      "Practice with code"
    ]
  },
  "report": {
    "gap_analysis": {                      // Structured gap analysis
      "total_gaps_identified": 3,
      "gaps_by_priority": {
        "high": ["Edge cases"],
        "medium": ["Optimization"],
        "low": []
      }
    },
    "learning_roadmap": [                  // Step-by-step path
      {
        "step": 1,
        "priority": "CRITICAL",
        "action": "Address misconceptions",
        "timeline": "Next session",
        "resources": [...]
      },
      {
        "step": 2,
        "priority": "HIGH",
        "action": "Master edge cases",
        "timeline": "This week",
        "resources": [...]
      }
    ]
  }
}
```

---

## 🎓 Mastery Levels

After evaluation, you'll see:

| Level | Score | Meaning |
|-------|-------|---------|
| **Beginner** | < 50% | Foundational understanding needed |
| **Developing** | 50-70% | Growing understanding, gaps remain |
| **Proficient** | 70-85% | Solid understanding, ready to advance |
| **Mastery** | 85%+ | Expert-level understanding achieved |

---

## 🚀 Advanced Features to Try

### 1. Mistake Injection Testing
- Respond strongly to several questions
- AI will occasionally inject subtle mistakes (15% probability)
- Try to catch and correct the mistakes!
- This tests and validates your real mastery

### 2. Topic Flexibility
Try teaching ANY topic:
- Science: "Photosynthesis is..."
- Math: "Calculus is..."
- Programming: "Object-oriented programming is..."
- History: "The Renaissance was..."
- Everything works!

### 3. Difficulty Progression
- Start with simple topics (Level 1)
- Give strong answers to progress to Level 2
- Continue strong performance to reach Level 3 (Expert)
- Watch AI questions get progressively harder

### 4. Mode Switching Strategies
- **Strong answers** → Stay in Student Mode (questions)
- **Weak answers** → Switch to Teacher Mode (clarification)
- **Partial answers** → Switch to Rescue Mode (hints)
- **Very strong** → Difficulty increases

### 5. Termination Offers
- When confidence > 75%, AI suggests ending
- You can:
  - Continue for harder challenges
  - End and get detailed evaluation
  - Your choice!

---

## 🔧 Troubleshooting

### "Error generating response"
**Solution:** Check GROQ_API_KEY in .env

### "Session not found"
**Solution:** Copy exact session_id from POST /session response

### "Connection failed"
**Solution:** MongoDB may be down (system falls back to in-memory)

### "Difficulty not progressing"
**Solution:** Need 2+ strong responses (avg quality > 0.75)

---

## 📚 Documentation Files

1. **COGNITIVE_SYSTEM.md** - Complete feature documentation
2. **TECHNICAL_GUIDE.md** - Architecture and implementation details
3. **IMPLEMENTATION_SUMMARY.md** - What was built and why
4. **This file** - Quick start guide

---

## 🎯 Success Tips

1. **Teach thoroughly** - Longer, detailed explanations score higher
2. **Use reasoning** - Include "because", "therefore", etc.
3. **Provide examples** - Concrete examples boost scores
4. **Watch for challenges** - AI will test your edge cases at higher levels
5. **Catch mistakes** - When AI injects errors, correct them!
6. **Review recommendations** - Learning roadmap tells you what to study next

---

## 🏆 Perfect Session Flow

```
1. Create session with your topic
2. Give detailed initial explanation
3. Answer AI's questions thoughtfully
4. Watch difficulty increase as you improve
5. If you struggle, AI switches to teaching mode
6. Continue to higher difficulties
7. When confident, AI offers to end
8. Request evaluation
9. Get comprehensive gap report
10. Follow personalized learning roadmap
```

---

## 📞 Support

For issues or questions:
1. Check the error logs (check_app.py for diagnostics)
2. Review TECHNICAL_GUIDE.md for detailed troubleshooting
3. Verify environment variables are set
4. Ensure MongoDB/Groq API are accessible

---

**Happy Learning! 🚀**

Curio AI - Where Teaching Is Learning.
