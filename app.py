import streamlit as st
import os
from gemini_client import GeminiClient
from knowledge_base import NCERTKnowledgeBase
from quiz_generator import QuizGenerator
from conversation_memory import ConversationMemory

# Initialize session state
if 'conversation_memory' not in st.session_state:
    st.session_state.conversation_memory = ConversationMemory()

if 'gemini_client' not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        st.session_state.gemini_client = GeminiClient(api_key)
    else:
        st.error("Please set GEMINI_API_KEY environment variable")
        st.stop()

if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = NCERTKnowledgeBase()

if 'quiz_generator' not in st.session_state:
    st.session_state.quiz_generator = QuizGenerator(st.session_state.gemini_client)

# Page configuration
st.set_page_config(
    page_title="AI Tutor for Indian Students",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and description
st.title("📚 AI Tutor for Indian Students")
st.markdown("*Your personalized NCERT curriculum assistant powered by AI*")

# Sidebar for navigation and settings
with st.sidebar:
    st.header("🎯 Features")
    
    feature = st.selectbox(
        "Choose a feature:",
        ["Ask Doubts", "Explain Topic", "Generate Quiz", "Homework Helper"]
    )
    
    st.header("📖 Subject & Class")
    
    class_level = st.selectbox(
        "Select Class:",
        ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]
    )
    
    subject = st.selectbox(
        "Select Subject:",
        ["Mathematics", "Science", "Social Science", "English", "Hindi"]
    )
    
    if st.button("Clear Conversation"):
        st.session_state.conversation_memory.clear()
        st.success("Conversation cleared!")
        st.rerun()

# Main content area
if feature == "Ask Doubts":
    st.header("❓ Ask Your Doubts")
    st.markdown("Ask any question from your NCERT syllabus and get detailed explanations!")
    
    # Display conversation history
    if st.session_state.conversation_memory.get_history():
        st.subheader("Previous Conversations:")
        for entry in st.session_state.conversation_memory.get_history()[-5:]:  # Show last 5
            with st.expander(f"Q: {entry['question'][:50]}..."):
                st.write(f"**Question:** {entry['question']}")
                st.write(f"**Answer:** {entry['answer']}")
                st.write(f"**Subject:** {entry.get('subject', 'N/A')} | **Class:** {entry.get('class', 'N/A')}")
    
    # Question input
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., Explain photosynthesis process in plants",
        height=100
    )
    
    if st.button("Get Answer", type="primary"):
        if question:
            with st.spinner("Generating answer..."):
                try:
                    # Get relevant context from knowledge base
                    context = st.session_state.knowledge_base.get_relevant_content(
                        question, subject, class_level
                    )
                    
                    # Generate answer using Gemini
                    answer = st.session_state.gemini_client.answer_question(
                        question, context, subject, class_level
                    )
                    
                    # Store in conversation memory
                    st.session_state.conversation_memory.add_conversation(
                        question, answer, subject, class_level
                    )
                    
                    # Display answer
                    st.success("Answer generated!")
                    st.markdown("### 💡 Answer:")
                    st.write(answer)
                    
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
        else:
            st.warning("Please enter a question!")

elif feature == "Explain Topic":
    st.header("📖 Topic Explanation")
    st.markdown("Get detailed explanations for any chapter or topic from your NCERT syllabus!")
    
    topic = st.text_input(
        "Enter topic or chapter name:",
        placeholder="e.g., Periodic Table, Quadratic Equations, Mughal Empire"
    )
    
    explanation_type = st.radio(
        "Type of explanation:",
        ["Summary", "Detailed", "Step-by-step"]
    )
    
    if st.button("Explain Topic", type="primary"):
        if topic:
            with st.spinner("Generating explanation..."):
                try:
                    # Get relevant content
                    context = st.session_state.knowledge_base.get_relevant_content(
                        topic, subject, class_level
                    )
                    
                    # Generate explanation
                    explanation = st.session_state.gemini_client.explain_topic(
                        topic, context, subject, class_level, explanation_type
                    )
                    
                    st.success("Explanation generated!")
                    st.markdown("### 📚 Explanation:")
                    st.write(explanation)
                    
                except Exception as e:
                    st.error(f"Error generating explanation: {str(e)}")
        else:
            st.warning("Please enter a topic!")

elif feature == "Generate Quiz":
    st.header("📝 Quiz Generator")
    st.markdown("Test your knowledge with AI-generated quizzes based on NCERT curriculum!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        chapter = st.text_input(
            "Chapter/Topic:",
            placeholder="e.g., Acids and Bases, Algebra"
        )
        
        num_questions = st.slider("Number of questions:", 3, 10, 5)
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty level:",
            ["Easy", "Medium", "Hard"]
        )
        
        question_type = st.selectbox(
            "Question type:",
            ["Multiple Choice", "True/False", "Short Answer"]
        )
    
    if st.button("Generate Quiz", type="primary"):
        if chapter:
            with st.spinner("Generating quiz..."):
                try:
                    quiz_data = st.session_state.quiz_generator.generate_quiz(
                        chapter, subject, class_level, num_questions, difficulty, question_type
                    )
                    
                    st.success("Quiz generated!")
                    st.markdown("### 📋 Quiz:")
                    
                    # Store quiz in session state for answering
                    st.session_state.current_quiz = quiz_data
                    
                    # Display quiz questions
                    for i, question in enumerate(quiz_data['questions'], 1):
                        st.markdown(f"**Question {i}:** {question['question']}")
                        
                        if question_type == "Multiple Choice":
                            options = question.get('options', [])
                            selected = st.radio(
                                f"Select answer for Question {i}:",
                                options,
                                key=f"q_{i}"
                            )
                        elif question_type == "True/False":
                            selected = st.radio(
                                f"Answer for Question {i}:",
                                ["True", "False"],
                                key=f"q_{i}"
                            )
                        else:  # Short Answer
                            selected = st.text_input(
                                f"Answer for Question {i}:",
                                key=f"q_{i}"
                            )
                    
                    if st.button("Submit Quiz"):
                        # Here you would implement quiz evaluation
                        st.info("Quiz submitted! (Evaluation feature can be implemented)")
                        
                except Exception as e:
                    st.error(f"Error generating quiz: {str(e)}")
        else:
            st.warning("Please enter a chapter or topic!")

elif feature == "Homework Helper":
    st.header("📝 Homework Helper")
    st.markdown("Get step-by-step help with your homework problems!")
    
    problem = st.text_area(
        "Enter your homework problem:",
        placeholder="e.g., Solve: 2x + 5 = 15",
        height=150
    )
    
    help_type = st.selectbox(
        "Type of help needed:",
        ["Step-by-step solution", "Concept explanation", "Hint only", "Similar examples"]
    )
    
    if st.button("Get Help", type="primary"):
        if problem:
            with st.spinner("Generating help..."):
                try:
                    # Get relevant context
                    context = st.session_state.knowledge_base.get_relevant_content(
                        problem, subject, class_level
                    )
                    
                    # Generate homework help
                    help_response = st.session_state.gemini_client.provide_homework_help(
                        problem, context, subject, class_level, help_type
                    )
                    
                    st.success("Help generated!")
                    st.markdown("### 🎯 Homework Help:")
                    st.write(help_response)
                    
                except Exception as e:
                    st.error(f"Error generating help: {str(e)}")
        else:
            st.warning("Please enter your homework problem!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>🤖 Powered by Gemini AI | 📚 Based on NCERT Curriculum</p>
        <p><em>Making quality education accessible to all Indian students</em></p>
    </div>
    """,
    unsafe_allow_html=True
)
