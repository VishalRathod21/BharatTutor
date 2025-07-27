# AI Tutor for Indian Students

## Overview

This is an AI-powered tutoring application specifically designed for Indian students following the NCERT curriculum. The application provides personalized learning assistance through doubt-solving, topic explanations, quiz generation, and homework help across multiple subjects and class levels.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture built with Python and Streamlit, consisting of several key components that work together to provide an intelligent tutoring experience:

### Frontend Architecture
- **Streamlit Web Interface**: Provides an interactive web-based UI with sidebar navigation
- **Session State Management**: Maintains user context and component instances across interactions
- **Feature-based Navigation**: Organized around core learning activities (Ask Doubts, Explain Topic, Generate Quiz, Homework Helper)

### Backend Architecture
- **Modular Component Design**: Separate classes handle distinct responsibilities
- **AI Integration**: Uses Google's Gemini AI model for natural language processing
- **Memory System**: Maintains conversation context for personalized interactions
- **Knowledge Base**: Structured repository of NCERT curriculum content

## Key Components

### 1. GeminiClient (`gemini_client.py`)
- **Purpose**: Handles all AI model interactions using Google's Gemini 2.5 Flash model
- **Key Functions**: Question answering, topic explanations with curriculum-appropriate responses
- **Design Choice**: Centralized AI client for consistent model usage across features

### 2. NCERTKnowledgeBase (`knowledge_base.py`)
- **Purpose**: Stores and retrieves NCERT curriculum content
- **Structure**: Hierarchical organization by subject → class → topics/content
- **Current State**: Sample implementation with Mathematics and Science content for Classes 6-10
- **Expansion Ready**: Designed to accommodate full NCERT corpus

### 3. QuizGenerator (`quiz_generator.py`)
- **Purpose**: Creates customized quizzes based on curriculum content
- **Features**: Multiple question types (MCQ, True/False, Short Answer), difficulty levels
- **Integration**: Uses GeminiClient for dynamic quiz generation

### 4. ConversationMemory (`conversation_memory.py`)
- **Purpose**: Maintains conversation context and learning history
- **Features**: Conversation storage, context retrieval, related question detection
- **Benefits**: Enables personalized learning experiences and continuity

### 5. Main Application (`app.py`)
- **Purpose**: Orchestrates all components and provides the user interface
- **Session Management**: Initializes and maintains component instances
- **Feature Routing**: Handles navigation between different learning modes

## Data Flow

1. **User Interaction**: Student selects feature and provides input (question, topic, quiz parameters)
2. **Context Retrieval**: ConversationMemory provides relevant conversation history
3. **Knowledge Lookup**: NCERTKnowledgeBase retrieves curriculum-relevant content
4. **AI Processing**: GeminiClient processes the request with context and knowledge
5. **Response Generation**: AI generates age-appropriate, curriculum-aligned responses
6. **Memory Update**: ConversationMemory stores the interaction for future context

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for the user interface
- **Google GenAI**: AI model integration for natural language processing
- **Python Standard Library**: datetime, os, logging, json for basic functionality

### AI Model
- **Gemini 2.5 Flash**: Google's language model for generating educational content
- **API Key Required**: GEMINI_API_KEY environment variable must be set

## Deployment Strategy

### Environment Setup
- **API Key Configuration**: Requires GEMINI_API_KEY environment variable
- **Error Handling**: Application stops gracefully if API key is missing
- **Session Persistence**: Uses Streamlit's session state for component lifecycle

### Scalability Considerations
- **Memory Management**: ConversationMemory limits stored conversations (max 50)
- **Modular Design**: Components can be independently scaled or replaced
- **Knowledge Base Expansion**: Structure supports easy addition of more NCERT content

### Current Limitations
- **Knowledge Base**: Contains sample content, needs full NCERT corpus integration
- **No Persistent Storage**: Conversations reset on application restart
- **Single User**: No multi-user support or authentication

### Future Enhancement Opportunities
- **Database Integration**: Add persistent storage for user progress and conversations
- **Vector Store Integration**: Implement RAG with embeddings for better content retrieval
- **User Authentication**: Add user accounts and personalized learning paths
- **Analytics**: Track learning progress and provide insights