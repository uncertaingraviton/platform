# AI Problem Solver - Single Problem Mode

A simplified AI-powered web application that evaluates user solutions against a single global problem without progress tracking or user guidance.

## Features

### 🎯 **Single Global Problem**
- One active problem for all users
- Admin-controlled problem selection
- No individual user progress tracking
- Simple solution evaluation only

### 🤖 **AI-Powered Solution Evaluation**
- Intelligent evaluation of user-proposed solutions
- Keyword-based matching against reference frameworks
- Real-time feedback without hints or guidance
- No step-by-step completion tracking

### 💬 **Streamlined Chat Interface**
- Current problem display
- Solution input and evaluation
- Real-time streaming responses
- No progress visualization

## How It Works

1. **Single Problem**: All users see the same active problem
2. **Submit Solutions**: Users type solutions in the chat
3. **AI Evaluation**: The AI evaluates solutions against reference steps
4. **Simple Feedback**: Users receive evaluation without progress tracking
5. **Admin Control**: Administrators can change the active problem

## Problem Types

### Mathematics
- **Mathematical Sequence Problem**: Pattern recognition and sequence completion

### Business
- **Business Strategy Development**: Product launch strategy planning

### Programming
- **Algorithm Design Challenge**: Algorithm optimization and design

### Creative
- **Creative Story Development**: Story writing with structured approach

### Science
- **Scientific Experiment Design**: Experimental design and methodology

## Admin Functions

To change the active problem, use the admin endpoint:

```bash
POST /admin/set-problem
Body: {"problem_id": "desired_problem_id"}
```

Available problem IDs:
- `math_sequence` - Mathematical sequence problem
- `business_strategy` - Business strategy development
- `coding_algorithm` - Algorithm design challenge
- `creative_writing` - Creative story development
- `scientific_method` - Scientific experiment design

## Adding Custom Problems

To add your own problems, edit `backend/problems_config.py`:

```python
CUSTOM_PROBLEMS = [
    ProblemFramework(
        id="your_problem_id",
        title="Your Problem Title",
        description="Description of your problem",
        reference_steps=[
            "Step 1 description",
            "Step 2 description",
            "Step 3 description"
        ],
        required_steps=3,
        difficulty_level="beginner",  # beginner, intermediate, advanced
        category="your_category"
    )
]
```

## API Endpoints

- `POST /chat` - Chat with solution evaluation
- `POST /chat/stream` - Streaming chat with solution evaluation
- `GET /problem/current` - Get current active problem
- `GET /problems` - Get available problems (admin function)
- `POST /admin/set-problem` - Change active problem (admin only)

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend
```bash
npm install
npm run dev
```

## Technical Architecture

- **Backend**: FastAPI with Python
- **Frontend**: React with TypeScript
- **AI Integration**: OpenAI GPT-4o Mini
- **Problem Management**: In-memory single problem selection
- **Real-time Updates**: Server-sent events for streaming responses

## Key Differences from Full Version

This simplified version removes:
- ❌ User progress tracking
- ❌ Step-by-step completion
- ❌ Progress visualization
- ❌ User guidance and hints
- ❌ Individual user sessions
- ❌ Progress persistence

## Example Usage

1. Start the application
2. All users see the same active problem
3. Users type solutions in the chat
4. AI evaluates each solution independently
5. Users receive feedback without progress tracking
6. Admins can change the active problem when needed

## Commands

Users can type these commands in the chat:
- `"show problem"` - Display current problem information
- `"available problems"` - List all available problems
- Any other text is treated as a solution for evaluation

The system provides focused solution evaluation without the complexity of progress tracking or user guidance.