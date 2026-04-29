# Curio Frontend - Role Reversal Learning AI

A modern, interactive frontend for the Curio role-reversal learning platform where users teach an AI student and learn deeply through interactive questioning.

## 🎯 Features

### Core Learning Experience
- **Interactive Chat Interface**: Real-time conversation with Curio, an inquisitive AI student
- **Multiple Learning Modes**:
  - **Student Mode**: AI asks challenging questions to deepen understanding
  - **Rescue Mode**: Gentle hints and guided learning when stuck
  - **Evaluator Mode**: Comprehensive assessment and gap analysis
- **Topic Selection**: Choose from popular topics or enter custom topics
- **Feynman Technique**: Start by explaining concepts in your own words

### Advanced Features
- **Real-time Feedback**: AI responds with specific intent (question, hint, challenge, etc.)
- **Rescue/Hint System**: Multi-level hints to guide learning without giving answers
- **Intelligent Reports**: 
  - Confidence scoring
  - Gap identification
  - Strength recognition
  - Personalized feedback
- **Progress Tracking**: Session history and learning progression

### UI/UX
- **Modern Tailwind Design**: Clean, professional interface aligned with "Curio" brand
- **Interactive Components**:
  - Message bubbles with intent indicators
  - Mode toggle with tooltips
  - Animated progress indicators
  - Responsive modal dialogs
- **Accessibility**: Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## 📂 Project Structure

```
frontend/
├── app/
│   ├── globals.css          # Global Tailwind styles
│   ├── layout.js            # Root layout wrapper
│   └── page.js              # Main application (UPDATED)
├── components/
│   ├── ChatWindow.jsx       # Chat display with intent indicators
│   ├── InputBox.jsx         # Enhanced message input with rescue button
│   ├── ReportPanel.jsx      # Comprehensive learning report
│   ├── TopicSelector.jsx    # Topic selection modal
│   ├── ModeToggle.jsx       # Interactive mode switcher
│   └── RescueHint.jsx       # Rescue/hint system modal
├── utils/
│   └── api.js               # Backend API service client
├── package.json             # Dependencies
├── .env.local               # Backend API URL configuration
└── tailwind.config.js       # Tailwind CSS configuration
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Configuration

Create `.env.local` with backend API:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

Visit `http://localhost:3000` in your browser.

### Production Build

```bash
npm run build
npm start
```

## 🔌 API Integration

The frontend integrates with the Curio backend through REST API calls:

### Key Endpoints Used

1. **Create Session**
   - `POST /session`
   - Initializes a new learning session with topic

2. **Chat**
   - `POST /chat`
   - Sends user message, receives AI response with intent and metadata

3. **Evaluate**
   - `POST /evaluate`
   - Generates comprehensive learning report

4. **Report**
   - `GET /report/{sessionId}`
   - Fetches detailed session report

5. **Session Management**
   - `GET /session/{sessionId}` - Get session details
   - `POST /session/{sessionId}/end` - End session

See [utils/api.js](utils/api.js) for complete API client implementation.

## 🎨 Component Documentation

### ChatWindow
Displays conversation history with AI intent indicators.

**Props:**
- `messages`: Array of message objects

**Message Format:**
```javascript
{
  role: "user" | "ai",
  content: string,
  ai_intent?: "question" | "hint" | "challenge" | "acknowledgment",
  followups?: string[]
}
```

### InputBox
Textarea input with Send and Rescue buttons.

**Props:**
- `onSend`: Callback when message is sent
- `onRescue`: Callback when Rescue button is clicked

### TopicSelector
Modal for selecting learning topic.

**Props:**
- `isOpen`: Boolean to control visibility
- `onSelectTopic`: Callback with selected topic

**Features:**
- 6 preset topics
- Custom topic input
- Animated transitions

### ModeToggle
Interactive mode switcher with tooltips.

**Props:**
- `currentMode`: Current mode state
- `onModeChange`: Callback when mode changes

**Modes:**
- Student: Ask questions
- Rescue: Provide hints
- Evaluator: Generate report

### RescueHint
Modal for rescue/hint system.

**Props:**
- `isOpen`: Boolean to control visibility
- `onClose`: Callback to close modal
- `onApplyHint`: Callback with hint action
- `currentTopic`: Current topic

**Actions:**
- Break Down: Start with fundamentals
- Give Example: Real-world application
- Reset Approach: Start fresh

### ReportPanel
Displays learning analytics and feedback.

**Props:**
- `report`: Report object from backend
- `isSessionActive`: Boolean showing session state

**Report Format:**
```javascript
{
  confidence_score: number,      // 0-1
  score: number,                 // 0-100
  understanding: string,         // "Weak" | "Developing" | "Moderate" | "Strong"
  gaps: string[],               // Areas to improve
  strengths: string[],          // Demonstrated strengths
  feedback: string[],           // Actionable feedback
  progress_state: {
    messages_count: number,
    turns_count: number
  }
}
```

## 🌟 Key Features Implementation

### Real-time Chat Flow
1. User selects topic → Session created
2. AI prompts user to explain concept
3. User sends explanation
4. Backend AI validates and responds
5. Cycle continues until session ends
6. Report auto-generates on completion

### Mode Switching
- Modes affect AI response style
- User can switch mid-session
- Mode change confirmed with AI message

### Rescue System
- 3-level hint system
- Multiple action options
- Non-intrusive guidance
- Encouragement messaging

### Report Generation
- Automatic on session end
- Includes confidence scoring
- Identifies knowledge gaps
- Highlights strengths
- Provides actionable feedback

## 🎯 Styling & Theme

**Brand Colors:**
- Primary: Blue (`#2563EB`)
- Accent: Amber (`#D97706`)
- Success: Green (`#059669`)
- Background: Slate gradients

**Typography:**
- Headlines: Font-bold, tracking-tight
- Body: Regular weight, readable line-height
- Labels: Uppercase, tracking-wider

**Components:**
- Rounded corners: `rounded-2xl` to `rounded-3xl`
- Shadows: Subtle with `shadow-sm` to `shadow-2xl`
- Spacing: Consistent 4px/8px grid
- Responsive: Mobile-first, tablet breakpoints

## 🔄 Data Flow

```
TopicSelector
    ↓
CreateSession (Backend)
    ↓
ChatWindow Display ← Messages
    ↓
InputBox (User Input)
    ↓
POST /chat (Backend)
    ↓
AI Response → Update Messages & ReportPanel
    ↓
Session End → POST /evaluate
    ↓
Generate Report
```

## 🛠 Development Tips

### Adding New Topics
Edit the `presetTopics` array in `TopicSelector.jsx`:
```javascript
const presetTopics = [
  { id: "topic_id", label: "Topic Name", icon: "emoji" },
  // ...
];
```

### Customizing AI Responses
Modify response formatting in `page.js` `handleSend()`:
```javascript
const aiMessage = {
  role: "ai",
  content: response.ai_message,
  ai_intent: response.ai_intent || "question",
  followups: response.followups || [],
};
```

### Adjusting Hints
Update hint messages in `RescueHint.jsx`:
```javascript
const hints = {
  1: "Your hint here...",
  2: "Another hint...",
  3: "Final hint...",
};
```

## 🚨 Troubleshooting

### Frontend can't connect to backend
- Check backend is running on port 8000
- Verify `.env.local` has correct API URL
- Check browser console for CORS errors
- Ensure backend API endpoints are accessible

### Styling looks broken
- Run `npm install` to ensure all dependencies
- Clear browser cache
- Check Tailwind CSS is properly configured
- Verify no conflicting CSS

### Components not updating
- Check React state management
- Verify callback functions are wired correctly
- Use browser DevTools to inspect component state
- Check terminal for console errors

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Lucide Icons](https://lucide.dev)

## 🤝 Contributing

When adding features:
1. Keep components focused and reusable
2. Maintain Tailwind styling consistency
3. Update this documentation
4. Test with backend API responses
5. Ensure responsive design

## 📝 License

Part of the Curio AI project.

---

**Tagline:** You teach. AI questions. You learn deeply. 🎓
