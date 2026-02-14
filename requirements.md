# Requirements Document: SAARTHI AI - Voice-First Learning Mentor

## Introduction

SAARTHI AI is a voice-first conversational AI mentor designed to guide users through technical learning tasks using natural conversation. The system targets students, beginner developers, and first-time technology users in India who prefer speaking over typing and may be more comfortable in regional languages. The system provides step-by-step guidance through voice interaction while maintaining context across sessions and adapting to user needs.

## Glossary

- **SAARTHI_System**: The complete voice-first AI learning mentor application
- **Wake_Word_Detector**: Component that listens for and recognizes the user-defined activation phrase
- **Voice_Processor**: Component that handles speech-to-text and text-to-speech conversion
- **Conversation_Manager**: Component that manages dialogue flow and context
- **Task_Analyzer**: Component that breaks down learning goals into actionable steps
- **Memory_Store**: Component that persists user progress and conversation context
- **Summary_Generator**: Component that creates text summaries of learning sessions
- **Communication_Gateway**: Component that delivers summaries via WhatsApp or SMS
- **Language_Adapter**: Component that handles multilingual conversation support
- **Emotion_Detector**: Component that analyzes user sentiment and confidence levels
- **Learning_Session**: A continuous interaction period between user and system
- **Task_Step**: An individual actionable instruction within a learning task
- **User_Profile**: Stored information about user preferences, progress, and history

## Requirements

### Requirement 1: Wake Word Activation

**User Story:** As a user, I want to activate the AI mentor using my own custom wake word, so that I can start conversations naturally without touching my device.

#### Acceptance Criteria

1. WHEN the user first sets up the system, THE SAARTHI_System SHALL allow the user to define a custom wake word
2. WHEN the wake word is spoken, THE Wake_Word_Detector SHALL activate the system within 500 milliseconds
3. WHEN background noise is present, THE Wake_Word_Detector SHALL distinguish the wake word from ambient sound with at least 90% accuracy
4. WHEN the wake word is not detected within 30 seconds of user speech, THE SAARTHI_System SHALL remain in listening mode without false activation
5. WHERE the user wants to change the wake word, THE SAARTHI_System SHALL allow wake word reconfiguration through voice commands

### Requirement 2: Real-Time Voice Interaction

**User Story:** As a user, I want to have natural voice conversations with the AI mentor, so that I can learn without typing or reading long texts.

#### Acceptance Criteria

1. WHEN the user speaks after wake word activation, THE Voice_Processor SHALL convert speech to text within 1 second
2. WHEN the system responds, THE Voice_Processor SHALL convert text to natural-sounding speech within 1 second
3. WHEN the user pauses mid-sentence, THE SAARTHI_System SHALL wait 2 seconds before processing the incomplete input
4. WHEN network connectivity is lost, THE SAARTHI_System SHALL inform the user via voice and attempt to reconnect
5. WHEN the user speaks in a supported regional language, THE Language_Adapter SHALL process the input in that language

### Requirement 3: Task Decomposition and Guidance

**User Story:** As a user, I want the AI to break down my learning goals into clear steps, so that I can follow along without feeling overwhelmed.

#### Acceptance Criteria

1. WHEN the user states a learning goal, THE Task_Analyzer SHALL decompose it into discrete Task_Steps within 3 seconds
2. WHEN providing guidance, THE Conversation_Manager SHALL present one Task_Step at a time
3. WHEN the user completes a Task_Step, THE SAARTHI_System SHALL acknowledge completion and present the next step
4. WHEN the user requests clarification, THE Conversation_Manager SHALL provide additional explanation without moving to the next step
5. WHEN a learning goal cannot be decomposed, THE SAARTHI_System SHALL ask clarifying questions to understand the goal better

### Requirement 4: Context Memory and Progress Tracking

**User Story:** As a user, I want the system to remember my progress across sessions, so that I can continue learning where I left off.

#### Acceptance Criteria

1. WHEN a Learning_Session ends, THE Memory_Store SHALL persist the current progress and conversation context
2. WHEN the user starts a new Learning_Session, THE SAARTHI_System SHALL retrieve and present the last known progress
3. WHEN the user asks about previous sessions, THE Conversation_Manager SHALL access and summarize relevant historical context
4. WHEN the user completes a task, THE Memory_Store SHALL mark that task as completed in the User_Profile
5. WHEN storage capacity is reached, THE Memory_Store SHALL retain the most recent 90 days of session data

### Requirement 5: Emotion-Aware Response Adaptation

**User Story:** As a user, I want the AI to adjust its explanations based on my confusion or confidence, so that I get the right level of support.

#### Acceptance Criteria

1. WHEN the user expresses confusion, THE Emotion_Detector SHALL identify the sentiment and signal the Conversation_Manager
2. WHEN confusion is detected, THE Conversation_Manager SHALL simplify explanations and provide additional examples
3. WHEN the user expresses confidence, THE Conversation_Manager SHALL proceed at a faster pace with less detailed explanations
4. WHEN the user repeats the same question, THE SAARTHI_System SHALL recognize the pattern and offer alternative explanation approaches
5. WHEN the user expresses frustration, THE Conversation_Manager SHALL offer to break down the current step into smaller sub-steps

### Requirement 6: Automatic Summary Generation

**User Story:** As a user, I want to receive text summaries of my learning sessions, so that I can review what I learned later.

#### Acceptance Criteria

1. WHEN a Learning_Session ends, THE Summary_Generator SHALL create a text summary containing key steps and outcomes
2. WHEN generating summaries, THE Summary_Generator SHALL include completed Task_Steps and pending items
3. WHEN the summary is created, THE SAARTHI_System SHALL include timestamps and duration of the session
4. WHEN the user requests a summary mid-session, THE Summary_Generator SHALL create a partial summary of progress so far
5. WHEN generating summaries, THE Summary_Generator SHALL format the text for readability on mobile devices

### Requirement 7: WhatsApp Summary Delivery

**User Story:** As a user, I want to receive session summaries via WhatsApp, so that I can easily access and share my learning progress.

#### Acceptance Criteria

1. WHEN the user provides a WhatsApp number during setup, THE SAARTHI_System SHALL store it in the User_Profile
2. WHEN a Learning_Session ends, THE Communication_Gateway SHALL send the summary to the registered WhatsApp number within 30 seconds
3. WHEN WhatsApp delivery fails, THE Communication_Gateway SHALL retry up to 3 times with exponential backoff
4. WHEN the user has not provided a WhatsApp number, THE SAARTHI_System SHALL offer SMS delivery as an alternative
5. WHERE the user wants to change delivery preferences, THE SAARTHI_System SHALL allow configuration through voice commands

### Requirement 8: SMS Summary Delivery

**User Story:** As a user, I want to receive session summaries via SMS when WhatsApp is not available, so that I always have access to my learning progress.

#### Acceptance Criteria

1. WHEN the user provides a phone number during setup, THE SAARTHI_System SHALL store it in the User_Profile
2. WHEN WhatsApp delivery is not configured, THE Communication_Gateway SHALL send summaries via SMS
3. WHEN SMS character limits are exceeded, THE Communication_Gateway SHALL split the summary into multiple messages
4. WHEN SMS delivery fails, THE Communication_Gateway SHALL retry up to 3 times and inform the user via voice
5. WHEN both WhatsApp and SMS delivery fail, THE SAARTHI_System SHALL store the summary locally for later retrieval

### Requirement 9: Multilingual Conversation Support

**User Story:** As a user, I want to interact with the AI in my preferred regional language, so that I can learn comfortably without language barriers.

#### Acceptance Criteria

1. WHEN the user first interacts, THE SAARTHI_System SHALL detect the spoken language and configure the Language_Adapter accordingly
2. WHEN the user switches languages mid-conversation, THE Language_Adapter SHALL adapt to the new language within 2 seconds
3. THE Language_Adapter SHALL support Hindi, English, Tamil, Telugu, Bengali, and Marathi
4. WHEN providing technical terms, THE Conversation_Manager SHALL use the original English term followed by explanation in the user's language
5. WHEN generating summaries, THE Summary_Generator SHALL use the same language as the conversation

### Requirement 10: Safety and Autonomy Boundaries

**User Story:** As a user, I want the AI to guide me without taking control of my device, so that I remain in control of my learning and actions.

#### Acceptance Criteria

1. THE SAARTHI_System SHALL NOT execute commands or control device functions autonomously
2. THE SAARTHI_System SHALL provide guidance and instructions only, requiring user action for all tasks
3. WHEN the user asks for emotional support or therapy, THE SAARTHI_System SHALL decline and redirect to learning-focused conversation
4. WHEN the user requests device automation, THE SAARTHI_System SHALL explain that it provides guidance only
5. THE SAARTHI_System SHALL clearly communicate that it is a learning mentor, not a device assistant or emotional companion

### Requirement 11: Session Management

**User Story:** As a user, I want to start, pause, and end learning sessions naturally through voice, so that I can learn at my own pace.

#### Acceptance Criteria

1. WHEN the user says a pause command, THE SAARTHI_System SHALL save the current state and enter pause mode
2. WHEN in pause mode, THE SAARTHI_System SHALL resume upon wake word detection
3. WHEN the user says an end command, THE SAARTHI_System SHALL conclude the Learning_Session and trigger summary generation
4. WHEN no user input is detected for 5 minutes, THE SAARTHI_System SHALL ask if the user wants to continue or end the session
5. WHEN the user ends a session, THE Memory_Store SHALL persist all progress before shutdown

### Requirement 12: User Profile Management

**User Story:** As a user, I want the system to remember my preferences and learning history, so that I get a personalized experience.

#### Acceptance Criteria

1. WHEN a user first uses the system, THE SAARTHI_System SHALL create a new User_Profile
2. THE User_Profile SHALL store wake word, preferred language, contact information, and learning history
3. WHEN the user updates preferences, THE SAARTHI_System SHALL modify the User_Profile immediately
4. WHEN the user requests to view their profile, THE Conversation_Manager SHALL read out the stored preferences
5. WHERE the user wants to delete their data, THE SAARTHI_System SHALL remove all User_Profile information and confirm deletion
