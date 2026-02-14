# Design Document: SAARTHI AI - Voice-First Learning Mentor

## Overview

SAARTHI AI is a voice-first conversational AI learning mentor designed as a hackathon prototype. The system enables natural voice interaction for technical learning guidance, with support for multiple Indian regional languages. The architecture prioritizes simplicity and feasibility while maintaining core functionality for wake word activation, conversational guidance, context memory, and summary delivery.

### Design Philosophy

This design focuses on creating a working prototype suitable for hackathon development (24-48 hours). We prioritize:
- Using existing APIs and services over building from scratch
- Simple, clear data flow between components
- Minimal infrastructure complexity
- Core functionality over edge case handling
- Feasible implementation with readily available tools

### Key Design Decisions

1. **Voice Processing**: Use cloud-based speech APIs (Google Speech-to-Text, Azure Speech) for reliability and multilingual support
2. **Wake Word Detection**: Use lightweight on-device library (Porcupine, Snowboy) for low-latency activation
3. **Conversational AI**: Use LLM API (OpenAI GPT-4, Anthropic Claude) with structured prompting for task decomposition and guidance
4. **Memory**: Simple file-based or SQLite storage for prototype (can scale to database later)
5. **Communication**: Use Twilio API for both WhatsApp and SMS delivery
6. **Language Support**: Leverage multilingual capabilities of modern speech and LLM APIs

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Voice Input/Output)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Voice Interaction Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Wake Word    │  │ Speech-to-   │  │ Text-to-Speech  │  │
│  │ Detector     │  │ Text         │  │ Synthesizer     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      Reasoning Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Conversation │  │ Task         │  │ Emotion         │  │
│  │ Manager      │  │ Analyzer     │  │ Detector        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                       Memory Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Session      │  │ User Profile │  │ Progress        │  │
│  │ Store        │  │ Store        │  │ Tracker         │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Communication Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Summary      │  │ WhatsApp     │  │ SMS             │  │
│  │ Generator    │  │ Gateway      │  │ Gateway         │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Activation Flow**: Wake Word Detector → Voice Interaction Layer → Conversation Manager
2. **Conversation Flow**: Speech-to-Text → Conversation Manager → Task Analyzer → Emotion Detector → Conversation Manager → Text-to-Speech
3. **Memory Flow**: Conversation Manager ↔ Memory Layer (bidirectional)
4. **Summary Flow**: Conversation Manager → Summary Generator → Communication Gateway → User

## Components and Interfaces

### Voice Interaction Layer

#### Wake Word Detector

**Purpose**: Continuously listens for user-defined wake word to activate the system.

**Implementation Approach**:
- Use Porcupine Wake Word engine (free tier available, supports custom wake words)
- Runs locally on device for low latency
- Minimal CPU usage in listening mode

**Interface**:
```python
class WakeWordDetector:
    def initialize(wake_word: str) -> bool
    def start_listening() -> None
    def stop_listening() -> None
    def on_wake_word_detected(callback: Callable) -> None
    def update_wake_word(new_wake_word: str) -> bool
```

**Key Operations**:
- `initialize`: Loads wake word model and prepares audio input
- `start_listening`: Begins continuous audio monitoring
- `on_wake_word_detected`: Registers callback to trigger when wake word is heard
- `update_wake_word`: Changes the active wake word

#### Speech-to-Text Processor

**Purpose**: Converts user voice input to text for processing.

**Implementation Approach**:
- Use Google Cloud Speech-to-Text API or Azure Speech Services
- Supports streaming recognition for real-time processing
- Built-in multilingual support (Hindi, Tamil, Telugu, Bengali, Marathi, English)

**Interface**:
```python
class SpeechToTextProcessor:
    def initialize(language_code: str) -> bool
    def start_recognition() -> None
    def stop_recognition() -> str
    def set_language(language_code: str) -> None
    def on_partial_result(callback: Callable[[str], None]) -> None
    def on_final_result(callback: Callable[[str], None]) -> None
```

**Key Operations**:
- `start_recognition`: Begins listening and streaming audio to API
- `stop_recognition`: Ends recognition and returns final transcribed text
- `set_language`: Changes recognition language dynamically
- `on_partial_result`: Provides real-time transcription updates

#### Text-to-Speech Synthesizer

**Purpose**: Converts system responses to natural-sounding speech.

**Implementation Approach**:
- Use Google Cloud Text-to-Speech or Azure Speech Services
- Select natural-sounding voices for each supported language
- Stream audio output for low latency

**Interface**:
```python
class TextToSpeechSynthesizer:
    def initialize(language_code: str, voice_name: str) -> bool
    def synthesize(text: str) -> AudioStream
    def set_voice(language_code: str, voice_name: str) -> None
    def play_audio(audio: AudioStream) -> None
```

**Key Operations**:
- `synthesize`: Converts text to audio stream
- `set_voice`: Changes voice based on language preference
- `play_audio`: Plays synthesized audio through device speakers

### Reasoning Layer

#### Conversation Manager

**Purpose**: Orchestrates dialogue flow, maintains conversation context, and coordinates with other components.

**Implementation Approach**:
- Uses LLM API (GPT-4 or Claude) with structured system prompts
- Maintains conversation history in memory
- Implements state machine for session management (active, paused, ended)

**Interface**:
```python
class ConversationManager:
    def initialize(user_profile: UserProfile) -> None
    def process_user_input(text: str, emotion: EmotionState) -> str
    def start_session() -> Session
    def pause_session() -> None
    def resume_session() -> None
    def end_session() -> SessionSummary
    def get_conversation_history() -> List[Message]
```

**Key Operations**:
- `process_user_input`: Takes user text and emotion, returns system response
- `start_session`: Creates new learning session with context from user profile
- `end_session`: Concludes session and triggers summary generation

**System Prompt Structure**:
```
You are SAARTHI, a voice-first AI learning mentor for technical education.

Context:
- User: {user_name}
- Language: {language}
- Current Task: {current_task}
- Progress: {completed_steps}/{total_steps}
- Emotion: {detected_emotion}

Guidelines:
1. Break down complex tasks into simple steps
2. Present one step at a time
3. Adapt explanation depth based on user emotion
4. Use conversational, encouraging tone
5. For technical terms, provide term in English followed by explanation in user's language
6. Never take autonomous actions - only provide guidance
7. Decline therapy or emotional support requests

Current Step: {current_step}
User Input: {user_input}

Provide your response:
```

#### Task Analyzer

**Purpose**: Decomposes learning goals into actionable steps.

**Implementation Approach**:
- Uses LLM with specialized prompt for task decomposition
- Returns structured list of steps with dependencies
- Estimates complexity and time for each step

**Interface**:
```python
class TaskAnalyzer:
    def analyze_goal(goal: str, user_context: UserContext) -> TaskPlan
    def get_next_step(task_plan: TaskPlan, completed_steps: List[str]) -> TaskStep
    def simplify_step(step: TaskStep) -> List[TaskStep]
```

**Key Operations**:
- `analyze_goal`: Takes learning goal and returns structured task plan
- `get_next_step`: Determines next step based on progress
- `simplify_step`: Breaks down a step into smaller sub-steps when user is confused

**Task Decomposition Prompt**:
```
Decompose the following learning goal into clear, actionable steps:

Goal: {user_goal}
User Level: {beginner/intermediate/advanced}
Language: {language}

Requirements:
1. Each step should be a single, clear action
2. Steps should build on each other logically
3. Include verification points after complex steps
4. Estimate time for each step (in minutes)
5. Mark steps that require external resources

Output format:
{
  "task_name": "...",
  "total_steps": N,
  "steps": [
    {
      "step_number": 1,
      "description": "...",
      "estimated_time": M,
      "requires_resources": true/false,
      "verification": "..."
    },
    ...
  ]
}
```

#### Emotion Detector

**Purpose**: Analyzes user sentiment and confidence from speech patterns and word choice.

**Implementation Approach**:
- Uses LLM-based sentiment analysis on transcribed text
- Detects confusion, confidence, frustration, excitement
- Provides emotion state to Conversation Manager for response adaptation

**Interface**:
```python
class EmotionDetector:
    def detect_emotion(text: str, conversation_history: List[Message]) -> EmotionState
    def detect_confusion_pattern(history: List[Message]) -> bool
```

**Key Operations**:
- `detect_emotion`: Analyzes current input and returns emotion state
- `detect_confusion_pattern`: Identifies repeated questions or confusion signals

**Emotion States**:
```python
class EmotionState(Enum):
    CONFIDENT = "confident"
    NEUTRAL = "neutral"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
```

### Memory Layer

#### Session Store

**Purpose**: Persists conversation history and session state.

**Implementation Approach**:
- SQLite database for prototype (single file, no server needed)
- Stores messages, timestamps, and session metadata
- Implements 90-day retention policy

**Interface**:
```python
class SessionStore:
    def create_session(user_id: str, task_goal: str) -> Session
    def save_message(session_id: str, message: Message) -> None
    def get_session(session_id: str) -> Session
    def get_recent_sessions(user_id: str, limit: int) -> List[Session]
    def update_session_state(session_id: str, state: SessionState) -> None
    def cleanup_old_sessions(days: int) -> int
```

**Key Operations**:
- `create_session`: Initializes new learning session
- `save_message`: Appends message to session history
- `cleanup_old_sessions`: Removes sessions older than specified days

#### User Profile Store

**Purpose**: Manages user preferences, contact information, and learning history.

**Implementation Approach**:
- SQLite database with user table
- Stores wake word, language preference, contact info, learning statistics

**Interface**:
```python
class UserProfileStore:
    def create_profile(user_id: str) -> UserProfile
    def get_profile(user_id: str) -> UserProfile
    def update_wake_word(user_id: str, wake_word: str) -> None
    def update_language(user_id: str, language: str) -> None
    def update_contact_info(user_id: str, whatsapp: str, sms: str) -> None
    def delete_profile(user_id: str) -> bool
```

**Key Operations**:
- `create_profile`: Creates new user with default settings
- `update_*`: Modifies specific profile fields
- `delete_profile`: Removes all user data

#### Progress Tracker

**Purpose**: Tracks task completion and learning progress.

**Implementation Approach**:
- Maintains task state and completion status
- Records completed steps and pending items
- Calculates progress metrics

**Interface**:
```python
class ProgressTracker:
    def start_task(session_id: str, task_plan: TaskPlan) -> None
    def mark_step_complete(session_id: str, step_number: int) -> None
    def get_progress(session_id: str) -> ProgressState
    def get_pending_steps(session_id: str) -> List[TaskStep]
```

**Key Operations**:
- `start_task`: Initializes progress tracking for new task
- `mark_step_complete`: Records step completion
- `get_progress`: Returns current progress percentage and status

### Communication Layer

#### Summary Generator

**Purpose**: Creates readable text summaries of learning sessions.

**Implementation Approach**:
- Uses LLM to generate concise, structured summaries
- Formats for mobile readability
- Includes key accomplishments and next steps

**Interface**:
```python
class SummaryGenerator:
    def generate_summary(session: Session, progress: ProgressState) -> str
    def generate_partial_summary(session: Session, progress: ProgressState) -> str
    def format_for_mobile(summary: str) -> str
```

**Key Operations**:
- `generate_summary`: Creates full session summary
- `generate_partial_summary`: Creates mid-session progress summary
- `format_for_mobile`: Ensures proper formatting for SMS/WhatsApp

**Summary Template**:
```
📚 SAARTHI Learning Summary

Session: {task_name}
Duration: {duration} minutes
Date: {date}

✅ Completed:
{completed_steps}

⏳ Next Steps:
{pending_steps}

💡 Key Learnings:
{key_points}

Keep going! 🚀
```

#### WhatsApp Gateway

**Purpose**: Delivers summaries via WhatsApp using Twilio API.

**Implementation Approach**:
- Uses Twilio WhatsApp Business API
- Implements retry logic with exponential backoff
- Handles delivery status callbacks

**Interface**:
```python
class WhatsAppGateway:
    def initialize(twilio_account_sid: str, twilio_auth_token: str) -> None
    def send_message(to_number: str, message: str) -> DeliveryStatus
    def retry_failed_message(message_id: str) -> DeliveryStatus
```

**Key Operations**:
- `send_message`: Sends summary to WhatsApp number
- `retry_failed_message`: Attempts redelivery on failure

#### SMS Gateway

**Purpose**: Delivers summaries via SMS as fallback or primary method.

**Implementation Approach**:
- Uses Twilio SMS API
- Splits long messages into multiple SMS (160 char limit)
- Tracks delivery status

**Interface**:
```python
class SMSGateway:
    def initialize(twilio_account_sid: str, twilio_auth_token: str) -> None
    def send_message(to_number: str, message: str) -> List[DeliveryStatus]
    def split_message(message: str, max_length: int) -> List[str]
```

**Key Operations**:
- `send_message`: Sends summary via SMS, splitting if necessary
- `split_message`: Intelligently splits long text at sentence boundaries

## Data Models

### Core Data Structures

#### UserProfile
```python
@dataclass
class UserProfile:
    user_id: str
    wake_word: str
    preferred_language: str  # ISO 639-1 code (hi, en, ta, te, bn, mr)
    whatsapp_number: Optional[str]
    sms_number: Optional[str]
    created_at: datetime
    last_active: datetime
    total_sessions: int
    total_learning_time: int  # minutes
```

#### Session
```python
@dataclass
class Session:
    session_id: str
    user_id: str
    task_goal: str
    task_plan: Optional[TaskPlan]
    state: SessionState  # active, paused, ended
    started_at: datetime
    ended_at: Optional[datetime]
    messages: List[Message]
    language: str
```

#### Message
```python
@dataclass
class Message:
    message_id: str
    session_id: str
    role: str  # user, assistant
    content: str
    emotion: Optional[EmotionState]
    timestamp: datetime
```

#### TaskPlan
```python
@dataclass
class TaskPlan:
    task_name: str
    total_steps: int
    steps: List[TaskStep]
    created_at: datetime
```

#### TaskStep
```python
@dataclass
class TaskStep:
    step_number: int
    description: str
    estimated_time: int  # minutes
    requires_resources: bool
    verification: str
    completed: bool
    completed_at: Optional[datetime]
```

#### ProgressState
```python
@dataclass
class ProgressState:
    session_id: str
    task_plan: TaskPlan
    completed_steps: List[int]
    current_step: int
    progress_percentage: float
    time_spent: int  # minutes
```

#### DeliveryStatus
```python
@dataclass
class DeliveryStatus:
    message_id: str
    status: str  # sent, delivered, failed
    timestamp: datetime
    error_message: Optional[str]
```

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    wake_word TEXT NOT NULL,
    preferred_language TEXT NOT NULL,
    whatsapp_number TEXT,
    sms_number TEXT,
    created_at TIMESTAMP NOT NULL,
    last_active TIMESTAMP NOT NULL,
    total_sessions INTEGER DEFAULT 0,
    total_learning_time INTEGER DEFAULT 0
);

-- Sessions table
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    task_goal TEXT NOT NULL,
    task_plan_json TEXT,
    state TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    language TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Messages table
CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    emotion TEXT,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Progress table
CREATE TABLE progress (
    session_id TEXT PRIMARY KEY,
    current_step INTEGER NOT NULL,
    completed_steps_json TEXT NOT NULL,
    progress_percentage REAL NOT NULL,
    time_spent INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Delivery log table
CREATE TABLE delivery_log (
    message_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    delivery_method TEXT NOT NULL,
    to_number TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    error_message TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Wake word non-activation for non-wake-word speech

*For any* speech input that does not contain the configured wake word, the Wake_Word_Detector should not trigger system activation.

**Validates: Requirements 1.4**

### Property 2: Multilingual input processing

*For any* supported language (Hindi, English, Tamil, Telugu, Bengali, Marathi), when a user speaks in that language, the Language_Adapter should correctly process the input and the system should respond in the same language.

**Validates: Requirements 2.5, 9.1, 9.3**

### Property 3: Task decomposition produces valid task plans

*For any* learning goal provided by a user, the Task_Analyzer should produce a TaskPlan with at least one TaskStep, where each step has a description, estimated time, and verification criteria.

**Validates: Requirements 3.1**

### Property 4: Single step presentation

*For any* TaskPlan with multiple steps, when requesting the current step from the Conversation_Manager, exactly one TaskStep should be presented.

**Validates: Requirements 3.2**

### Property 5: Step progression on completion

*For any* TaskPlan with N steps where N > 1, when step M is marked complete (where M < N), the next presented step should be step M+1.

**Validates: Requirements 3.3**

### Property 6: Clarification preserves current step

*For any* active session at step N, when a clarification request is processed, the current step should remain N (no progression).

**Validates: Requirements 3.4**

### Property 7: Session data persistence round-trip

*For any* active session with progress data, ending the session and then retrieving it should produce equivalent session state including all messages, progress, and metadata.

**Validates: Requirements 4.1, 11.5**

### Property 8: Session resumption loads previous progress

*For any* user with at least one completed session, starting a new session should make the previous session's progress accessible to the Conversation_Manager.

**Validates: Requirements 4.2**

### Property 9: Historical context retrieval

*For any* user with session history, querying for previous sessions should return a list of sessions ordered by recency with accurate metadata.

**Validates: Requirements 4.3**

### Property 10: Task completion updates profile

*For any* task in a session, when marked as complete, the User_Profile should reflect the completion in its learning history.

**Validates: Requirements 4.4**

### Property 11: Confusion detection triggers emotion state

*For any* user input containing confusion indicators (phrases like "I don't understand", "what does that mean", "confused"), the Emotion_Detector should identify the emotion as CONFUSED.

**Validates: Requirements 5.1**

### Property 12: Emotion-aware response adaptation

*For any* user emotion state (CONFUSED, CONFIDENT, FRUSTRATED), the Conversation_Manager should adapt response complexity accordingly: CONFUSED → more detailed, CONFIDENT → more concise, FRUSTRATED → offer simplification.

**Validates: Requirements 5.2, 5.3**

### Property 13: Repeated question pattern detection

*For any* sequence of messages where the same question appears 3 or more times, the system should detect the repetition pattern and offer an alternative explanation approach.

**Validates: Requirements 5.4**

### Property 14: Summary contains required elements

*For any* completed session, the generated summary should contain: task name, completed steps list, pending steps list, session duration, and timestamps.

**Validates: Requirements 6.1, 6.2, 6.3**

### Property 15: Partial summary generation

*For any* active (non-ended) session with at least one completed step, requesting a summary should produce a valid partial summary containing progress so far.

**Validates: Requirements 6.4**

### Property 16: Mobile-friendly summary formatting

*For any* generated summary, the text should have line length ≤ 80 characters, use clear section markers (emoji or symbols), and avoid complex formatting.

**Validates: Requirements 6.5**

### Property 17: Profile data persistence

*For any* User_Profile with wake_word, preferred_language, and contact information set, storing and then retrieving the profile should produce equivalent data.

**Validates: Requirements 7.1, 8.1, 12.2**

### Property 18: SMS message splitting

*For any* summary text longer than 160 characters, the SMS_Gateway should split it into multiple messages where each message is ≤ 160 characters and splits occur at sentence boundaries when possible.

**Validates: Requirements 8.3**

### Property 19: Language switching updates adapter

*For any* active session in language L1, when the user switches to language L2 (where L2 is supported), the Language_Adapter should update its configuration to L2 and subsequent responses should be in L2.

**Validates: Requirements 9.2**

### Property 20: Technical term formatting

*For any* response containing technical terms, the text should follow the pattern: English_Term (explanation in user's language), ensuring technical vocabulary is preserved while providing translation.

**Validates: Requirements 9.4**

### Property 21: Summary language consistency

*For any* session conducted in language L, the generated summary should be in the same language L.

**Validates: Requirements 9.5**

### Property 22: Guidance-only responses

*For any* system response, the text should contain instructional language (e.g., "you should", "try this", "next step is") and should not contain action verbs indicating autonomous system behavior (e.g., "I will execute", "I am running").

**Validates: Requirements 10.2**

### Property 23: Boundary request rejection

*For any* user request for emotional support, therapy, or device automation, the system response should contain a polite decline and redirect to learning-focused topics.

**Validates: Requirements 10.3, 10.4**

### Property 24: Pause preserves session state

*For any* active session at step N with M completed steps, pausing the session should change the session state to PAUSED and preserve both current step N and completed steps M.

**Validates: Requirements 11.1**

### Property 25: Session end triggers summary

*For any* active session, when the end command is processed, the session state should change to ENDED and a summary should be generated.

**Validates: Requirements 11.3**

### Property 26: Profile update immediacy

*For any* User_Profile field (wake_word, language, contact info), when an update is requested, retrieving the profile immediately after should reflect the new value.

**Validates: Requirements 12.3**

## Error Handling

### Voice Processing Errors

**Network Failures**:
- Speech-to-Text API unavailable: Inform user via pre-cached voice message, suggest trying again
- Text-to-Speech API unavailable: Fall back to text display if UI available, otherwise queue response for later
- Retry strategy: 3 attempts with exponential backoff (1s, 2s, 4s)

**Audio Input Errors**:
- Microphone not accessible: Display error message and request permissions
- No speech detected: After 10 seconds of silence, prompt user with "I'm listening, please speak"
- Unclear speech: Ask user to repeat with "I didn't catch that, could you say it again?"

### Task Analysis Errors

**Vague Goals**:
- When Task_Analyzer cannot decompose goal: Ask 2-3 clarifying questions
- Example: "I want to learn coding" → "What type of coding? Web development, mobile apps, or something else?"

**Unsupported Topics**:
- When goal is outside technical learning domain: Politely explain scope limitations
- Redirect to supported topics: "I specialize in technical learning. I can help with programming, web development, data analysis..."

### Memory and Storage Errors

**Database Errors**:
- Write failure: Retry up to 3 times, if all fail, cache in memory and warn user
- Read failure: Return empty/default data and log error
- Corruption: Attempt recovery, if impossible, create new profile and notify user

**Storage Full**:
- When disk space low: Trigger cleanup of old sessions (>90 days)
- If still full: Warn user and operate in memory-only mode

### Communication Errors

**WhatsApp Delivery Failures**:
- Invalid number: Validate format before sending, prompt user to correct
- API error: Retry 3 times with exponential backoff (5s, 10s, 20s)
- All retries failed: Fall back to SMS delivery

**SMS Delivery Failures**:
- Invalid number: Validate format, prompt correction
- API error: Retry 3 times
- All retries failed: Store summary locally, inform user via voice

**Both Delivery Methods Failed**:
- Store summary in local database
- Inform user: "I couldn't send the summary, but I've saved it. You can ask me to read it anytime."
- Provide voice option to read summary aloud

### Language Processing Errors

**Unsupported Language Detected**:
- Inform user of supported languages
- Ask user to choose from: Hindi, English, Tamil, Telugu, Bengali, Marathi
- Default to English if no choice made

**Language Detection Ambiguity**:
- When confidence < 70%: Ask user "Are you speaking in [detected_language]?"
- Allow user to explicitly set language

**Translation Errors**:
- When technical term has no good translation: Use English term with explanation
- Example: "API (a way for programs to talk to each other)"

### Session Management Errors

**Concurrent Session Conflict**:
- Only one active session per user allowed
- If new session requested while one active: Ask "You have an active session. End it or continue?"

**Session Recovery Failure**:
- If corrupted session data: Start fresh session, log error
- Inform user: "I couldn't load your previous session, let's start fresh."

### Wake Word Detection Errors

**False Positives**:
- If activated without wake word: Implement confidence threshold (>80%)
- Log false positives for model improvement

**Wake Word Not Detected**:
- Ensure continuous listening mode
- If user reports issues: Offer to re-record wake word with better audio quality

## Testing Strategy

### Overview

SAARTHI AI requires a dual testing approach combining unit tests for specific scenarios and property-based tests for universal correctness guarantees. Given the voice-first nature and external API dependencies, testing focuses on business logic, data flow, and integration points while mocking external services.

### Testing Approach

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Focus on: specific user flows, error handling, boundary conditions
- Mock external APIs (speech, LLM, Twilio)
- Test individual component behavior

**Property-Based Tests**: Verify universal properties across all inputs
- Focus on: data persistence, state transitions, language handling
- Generate random valid inputs to test properties
- Minimum 100 iterations per property test
- Each test references design document property

**Integration Tests**: Verify component interactions
- Test data flow between layers
- Verify API integration with real services (in staging)
- Test end-to-end user scenarios

### Property-Based Testing Configuration

**Framework Selection**:
- Python: Use `hypothesis` library
- TypeScript: Use `fast-check` library
- Configuration: Minimum 100 test iterations per property

**Test Tagging Format**:
Each property test must include a comment tag:
```python
# Feature: saarthi-ai-mentor, Property 7: Session data persistence round-trip
```

**Property Test Implementation**:
- Each correctness property (1-26) should have exactly ONE property-based test
- Tests should generate random valid inputs within domain constraints
- Tests should verify the property holds across all generated inputs

### Test Coverage by Component

#### Voice Interaction Layer

**Wake Word Detector**:
- Unit tests:
  - Test wake word initialization with valid/invalid words
  - Test callback registration and triggering
  - Test wake word update functionality
- Property tests:
  - Property 1: Non-wake-word speech doesn't trigger activation

**Speech-to-Text Processor**:
- Unit tests:
  - Test initialization with different languages
  - Test language switching
  - Test error handling for API failures
- Property tests:
  - Property 2: Multilingual input processing (test all supported languages)

**Text-to-Speech Synthesizer**:
- Unit tests:
  - Test voice selection for different languages
  - Test audio streaming
  - Test error handling for API failures

#### Reasoning Layer

**Conversation Manager**:
- Unit tests:
  - Test session start/pause/resume/end flows
  - Test network error handling
  - Test timeout behavior
  - Test boundary request rejection (therapy, automation)
- Property tests:
  - Property 4: Single step presentation
  - Property 6: Clarification preserves current step
  - Property 12: Emotion-aware response adaptation
  - Property 22: Guidance-only responses
  - Property 23: Boundary request rejection
  - Property 24: Pause preserves session state
  - Property 25: Session end triggers summary

**Task Analyzer**:
- Unit tests:
  - Test vague goal handling
  - Test unsupported topic handling
  - Test step simplification
- Property tests:
  - Property 3: Task decomposition produces valid task plans
  - Property 5: Step progression on completion

**Emotion Detector**:
- Unit tests:
  - Test specific confusion phrases
  - Test specific confidence phrases
  - Test specific frustration phrases
- Property tests:
  - Property 11: Confusion detection triggers emotion state
  - Property 13: Repeated question pattern detection

#### Memory Layer

**Session Store**:
- Unit tests:
  - Test session creation
  - Test message appending
  - Test 90-day cleanup
  - Test database error handling
- Property tests:
  - Property 7: Session data persistence round-trip
  - Property 8: Session resumption loads previous progress
  - Property 9: Historical context retrieval

**User Profile Store**:
- Unit tests:
  - Test profile creation with defaults
  - Test profile deletion
  - Test invalid data handling
- Property tests:
  - Property 17: Profile data persistence
  - Property 26: Profile update immediacy

**Progress Tracker**:
- Unit tests:
  - Test progress calculation
  - Test step completion marking
  - Test pending steps retrieval
- Property tests:
  - Property 10: Task completion updates profile

#### Communication Layer

**Summary Generator**:
- Unit tests:
  - Test summary generation with empty session
  - Test summary generation with very long sessions
  - Test mobile formatting edge cases
- Property tests:
  - Property 14: Summary contains required elements
  - Property 15: Partial summary generation
  - Property 16: Mobile-friendly summary formatting
  - Property 21: Summary language consistency

**WhatsApp Gateway**:
- Unit tests:
  - Test invalid number handling
  - Test retry logic with mock failures
  - Test delivery status tracking
- Integration tests:
  - Test actual WhatsApp delivery (staging environment)

**SMS Gateway**:
- Unit tests:
  - Test invalid number handling
  - Test retry logic
  - Test delivery status tracking
- Property tests:
  - Property 18: SMS message splitting
- Integration tests:
  - Test actual SMS delivery (staging environment)

#### Language Support

**Language Adapter**:
- Unit tests:
  - Test unsupported language handling
  - Test language detection ambiguity
  - Test technical term formatting
- Property tests:
  - Property 2: Multilingual input processing (covered above)
  - Property 19: Language switching updates adapter
  - Property 20: Technical term formatting

### Test Data Generation

**For Property-Based Tests**:

Generate random valid instances of:
- User profiles with various language preferences
- Sessions with varying numbers of messages and steps
- Task plans with 1-10 steps
- Summaries of different lengths
- Phone numbers in valid formats
- Emotion states (all enum values)
- Supported language codes

**Constraints for Generators**:
- User IDs: UUID format
- Phone numbers: Valid international format (+91XXXXXXXXXX)
- Languages: Only from supported set (hi, en, ta, te, bn, mr)
- Wake words: 2-4 syllables, pronounceable
- Session durations: 1-120 minutes
- Task steps: 1-20 per plan

### Mock Strategy

**External APIs to Mock**:
- Google/Azure Speech-to-Text API
- Google/Azure Text-to-Speech API
- OpenAI/Anthropic LLM API
- Twilio WhatsApp API
- Twilio SMS API
- Porcupine Wake Word engine

**Mock Behaviors**:
- Success cases with realistic latency simulation
- Failure cases (network errors, API errors, rate limits)
- Partial failures (some retries succeed)

### Integration Testing

**Staging Environment**:
- Use real APIs with test credentials
- Test end-to-end flows:
  1. Wake word → conversation → task completion → summary delivery
  2. Multi-session user journey
  3. Language switching mid-conversation
  4. Error recovery flows

**Performance Testing**:
- Measure response latency (target: <2s for full conversation turn)
- Test with concurrent users (target: 10 concurrent sessions)
- Test with large session histories (target: 100+ sessions per user)

### Continuous Testing

**Pre-commit Hooks**:
- Run unit tests
- Run fast property tests (10 iterations)

**CI Pipeline**:
- Run all unit tests
- Run full property tests (100 iterations)
- Run integration tests against staging
- Generate coverage report (target: >80% for business logic)

**Manual Testing**:
- Voice interaction testing with real users
- Multilingual testing with native speakers
- Usability testing for target audience (students, beginners)
