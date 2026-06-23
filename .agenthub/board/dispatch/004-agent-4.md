---
author: coordinator
timestamp: 2026-06-09T00:00:00Z
channel: dispatch
parent: null
---

# Agent 4: Prototype - Build MVP Task

## Role
Full-stack engineer building a working MVP of the voice receptionist system.

## Task

Build a complete, working prototype of the AI voice receptionist for real estate agents.

### Deliverables

#### 1. Project Structure
Create `projects/voice-receptionist/` with:

```
projects/voice-receptionist/
├── README.md                    # Setup and usage guide
├── ARCHITECTURE.md              # (from Agent 1)
├── TECH_STACK.md               # (from Agent 2)
├── INTEGRATION.md              # (from Agent 3)
├── src/
│   ├── __init__.py
│   ├── voice_processor.py       # Main voice pipeline
│   ├── conversation_manager.py  # State machine + context
│   ├── intent_detector.py       # Claude-based intent logic
│   ├── action_executor.py       # Bridge integration
│   ├── database.py              # SQLite persistence
│   └── api.py                   # Flask endpoints
├── tests/
│   ├── __init__.py
│   ├── test_voice_processor.py
│   ├── test_conversation_manager.py
│   ├── test_intent_detector.py
│   ├── test_action_executor.py
│   └── test_integration.py
├── example_calls.py             # Simulated call scenarios
├── requirements.txt
├── voice_receptionist.db        # SQLite database (created on first run)
└── .env.example
```

#### 2. Core Modules

**voice_processor.py**
- Simulates phone input (accept transcribed text as input)
- Call state tracking
- Interaction orchestration
- Response generation

**conversation_manager.py**
- Implement state machine from Agent 1 design
- Maintain conversation context and history
- Track conversation turns
- Handle state transitions

**intent_detector.py**
- Use Claude API to detect intent from user input
- Supported intents: schedule_appointment, take_message, qualify_lead, property_info
- Return structured intent object with extracted parameters

**action_executor.py**
- Make HTTP calls to localhost:5000 or localhost:9000
- Execute appointments, messages, qualification, info queries
- Handle responses and errors
- Log results to database

**database.py**
- SQLite schema from Agent 1
- CRUD operations for calls, leads, conversations, appointments
- Connection pooling
- Migration support

**api.py**
- Flask endpoint for receiving transcribed text
- POST /api/calls/{call_id}/input
- GET /api/calls/{call_id}/status
- GET /api/leads
- GET /api/calls (with filtering)

#### 3. Three Core Flows (Fully Implemented)

**Flow 1: Schedule Appointment**
```
User: "I'd like to schedule an appointment with the agent"
System: [intent: schedule_appointment] 
System: "I'd be happy to help schedule an appointment. What date and time work best for you?"
User: "Friday at 2pm"
System: [extract datetime, check availability via Bridge]
System: "Perfect, I've scheduled you for Friday at 2pm. We'll send you a confirmation email."
[Log to appointments table, notify agent]
```

**Flow 2: Take Message**
```
User: "I have a question about the property listing"
System: [intent: take_message]
System: "I'd be happy to pass that along to the agent. What's your message?"
User: "[detailed question]"
System: [intent: take_message confirmation]
System: "Got it, I'll make sure the agent gets your message right away."
[Log to messages table]
```

**Flow 3: Qualify Lead**
```
User: "I'm interested in buying a home in the area"
System: [intent: qualify_lead]
System: "Great! I'd like to ask a few questions. What's your budget range?"
User: "Between $500k and $750k"
System: [ask follow-ups: timeline, property type, location]
User: "[answers]"
System: [score lead, route appropriately]
System: "Thank you for that information. An agent will contact you shortly."
[Log to leads table with score]
```

#### 4. Integration Layer
- HTTP client to call localhost:5000/9000
- Convert voice receptionist actions → skill bridge calls
- Handle integration errors gracefully
- Log all bridge interactions

#### 5. Test Suite
Comprehensive tests covering:
- Voice processor receives input and generates responses
- Conversation manager maintains state correctly
- Intent detection works for all 4 intents
- State transitions happen as designed
- HTTP calls to Bridge are properly formatted
- Database operations work (CRUD)
- Error cases handled (bridge timeout, invalid input, etc.)

Minimum 15 test cases, all passing.

#### 6. Example Call Scenarios
Create `example_calls.py` demonstrating:
- Complete appointment scheduling call (5-6 turns)
- Complete message-taking call (4-5 turns)
- Complete lead qualification call (6-8 turns)
- Complete property info query (3-4 turns)

Can be simulated (no actual phone system needed) - just transcribed text inputs.

#### 7. README
Include:
- System overview and architecture
- Installation instructions (pip install -r requirements.txt)
- Database setup (python -m src.database --init)
- Running the Flask API (python src/api.py)
- Running tests (pytest tests/)
- Example usage (python example_calls.py)
- How to interact with Bridge (test against localhost:5000/9000)
- Troubleshooting guide

### Implementation Notes

**Claude Integration**
- Use Claude 3.5 Sonnet for intent detection
- System prompt: "You are a voice receptionist for a real estate agent. Detect the user's intent and extract relevant parameters..."
- Call Claude synchronously in intent_detector.py
- Budget ~2-3 API calls per user turn

**State Machine**
- Implement as enum-based state class
- Support transitions: greeting → intent → action → confirm → end
- Store current state in conversation context
- Use Agent 1's state diagram

**Database**
- SQLite (no external dependencies)
- Tables: calls, leads, conversations, appointments
- Foreign key relationships
- Timestamps on all records

**Bridge Integration**
- Use requests library for HTTP
- Handle connection errors with retry logic (3 attempts, exponential backoff)
- Log all requests and responses
- Mock localhost:5000 responses for testing

**No Phone System Required**
- This is a prototype, not production-ready
- Accept text input (simulating Twilio/other transcription)
- Respond with text output (response text)
- Can later add real phone integration

### Success Criteria
- All code runs without errors
- Tests pass (pytest output shows green)
- 3 core flows work end-to-end
- Integration layer can make HTTP calls
- Database persists data correctly
- README allows someone to set up and run in <10 minutes
- Code is clean, documented, and follows Python best practices

## Notes
- Use Agent 1's ARCHITECTURE.md as spec
- Use Agent 2's TECH_STACK.md for library decisions
- Use Agent 3's INTEGRATION.md for Bridge API contracts
- Work in your isolated worktree
- Commit all code with descriptive messages
- Write your result summary to `.agenthub/board/results/agent-4-result.md`
