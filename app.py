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
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Main title and description with enhanced styling
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🎓 AI Tutor for Indian Students</h1>
    <p style="font-size: 1.2rem; color: #b0b0b0; font-weight: 300;">
        Your personalized NCERT curriculum assistant powered by advanced AI
    </p>
    <div style="width: 100px; height: 3px; background: linear-gradient(45deg, #00ff88, #00b4ff); margin: 1rem auto; border-radius: 2px;"></div>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar with modern styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #00ff88; margin-bottom: 0.5rem;">🎯 Learning Hub</h2>
        <div style="width: 50px; height: 2px; background: linear-gradient(45deg, #00ff88, #00b4ff); margin: 0 auto; border-radius: 1px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature selection with enhanced styling
    st.markdown("### 🚀 Choose Feature")
    feature = st.selectbox(
        "Select learning mode:",
        ["Ask Doubts", "Explain Topic", "Generate Quiz", "Homework Helper"],
        help="Choose what you'd like to do today"
    )
    
    st.markdown("---")
    
    # Academic settings
    st.markdown("### 📚 Academic Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        class_level = st.selectbox(
            "Class:",
            ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"],
            help="Select your current class"
        )
    
    with col2:
        subject = st.selectbox(
            "Subject:",
            ["Mathematics", "Science", "Social Science", "English", "Hindi"],
            help="Choose the subject you need help with"
        )
    
    st.markdown("---")
    
    # Action buttons
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", help="Clear conversation history"):
            st.session_state.conversation_memory.clear()
            st.success("Conversation cleared!")
            st.rerun()
    
    with col2:
        if st.button("📊 Stats", help="View learning statistics"):
            stats = st.session_state.conversation_memory.get_statistics()
            if stats['total_conversations'] > 0:
                st.json(stats)
            else:
                st.info("No conversations yet!")
    
    # Progress indicator
    st.markdown("---")
    st.markdown("### 📈 Your Progress")
    
    total_conversations = len(st.session_state.conversation_memory.get_history())
    if total_conversations > 0:
        st.metric("Questions Asked", total_conversations)
        
        # Subject breakdown
        stats = st.session_state.conversation_memory.get_statistics()
        if 'subjects_used' in stats:
            most_active = stats.get('most_active_subject', 'None')
            st.metric("Favorite Subject", most_active)
    else:
        st.info("Start learning to see your progress!")

# Main content area with modern styling
if feature == "Ask Doubts":
    # Feature header with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2a2a2a, #1a1a1a); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #333;">
        <h2 style="color: #00ff88; margin-bottom: 0.5rem; display: flex; align-items: center;">
            ❓ Ask Your Doubts
        </h2>
        <p style="color: #b0b0b0; margin: 0; font-size: 1.1rem;">
            Get instant, detailed explanations for any question from your NCERT syllabus
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab2 = st.tabs(["💬 Ask Question", "📚 Recent Conversations"])
    
    with tab2:
        if st.session_state.conversation_memory.get_history():
            st.markdown("### 🕒 Your Learning History")
            
            # Display conversation history with enhanced styling
            for i, entry in enumerate(st.session_state.conversation_memory.get_history()[-5:][::-1]):  # Show last 5, newest first
                with st.expander(f"Q{len(st.session_state.conversation_memory.get_history())-i}: {entry['question'][:60]}{'...' if len(entry['question']) > 60 else ''}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**🤔 Question:**")
                        st.write(entry['question'])
                        st.markdown(f"**💡 Answer:**")
                        st.write(entry['answer'])
                    with col2:
                        st.markdown(f"**📚 Subject:** {entry.get('subject', 'N/A')}")
                        st.markdown(f"**🎓 Class:** {entry.get('class', 'N/A')}")
                        st.markdown(f"**⏰ Time:** {entry.get('timestamp', 'N/A')[:16]}")
        else:
            st.info("🌟 No previous conversations yet. Start by asking your first question!")
    
    with tab1:
        st.markdown("### 🤔 What would you like to learn?")
        
        # Enhanced question input with tips
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_area(
                "Enter your question:",
                placeholder="e.g., Explain photosynthesis process in plants\nWhat is the quadratic formula?\nHow does the human digestive system work?",
                height=120,
                help="Ask any question related to your NCERT syllabus"
            )
        
        with col2:
            st.markdown("**💡 Tips for better answers:**")
            st.markdown("• Be specific about the topic")
            st.markdown("• Mention the chapter if known")
            st.markdown("• Ask for examples if needed")
            st.markdown("• Request step-by-step explanations")
    
        st.markdown("---")
        
        # Enhanced action button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Get Answer", type="primary", use_container_width=True):
                if question:
                    with st.spinner("🤖 AI is thinking... Please wait"):
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
                            
                            # Display answer with enhanced styling
                            st.success("✅ Answer generated successfully!")
                            
                            # Enhanced answer display
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 2rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #00ff88;">
                                <h3 style="color: #00ff88; margin-bottom: 1rem;">💡 Your Answer</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(answer)
                            
                            # Add feedback options
                            st.markdown("---")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("👍 Helpful"):
                                    st.success("Thank you for your feedback!")
                            with col2:
                                if st.button("👎 Not helpful"):
                                    st.info("We'll improve! Try rephrasing your question.")
                            with col3:
                                if st.button("🔄 Ask follow-up"):
                                    st.info("Feel free to ask a related question!")
                            
                        except Exception as e:
                            st.error(f"❌ Error generating answer: {str(e)}")
                            st.info("💡 Try rephrasing your question or check your internet connection.")
                else:
                    st.warning("⚠️ Please enter a question to get started!")

elif feature == "Explain Topic":
    # Feature header with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2a2a2a, #1a1a1a); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #333;">
        <h2 style="color: #00b4ff; margin-bottom: 0.5rem; display: flex; align-items: center;">
            📖 Topic Explanation
        </h2>
        <p style="color: #b0b0b0; margin: 0; font-size: 1.1rem;">
            Get comprehensive explanations for any chapter or topic from your NCERT curriculum
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section with better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Enter Topic Details")
        topic = st.text_input(
            "Topic or chapter name:",
            placeholder="e.g., Periodic Table, Quadratic Equations, Mughal Empire, Photosynthesis",
            help="Enter the specific topic you want to learn about"
        )
    
    with col2:
        st.markdown("### 🎯 Explanation Style")
        explanation_type = st.radio(
            "Choose explanation type:",
            ["Summary", "Detailed", "Step-by-step"],
            help="Select how detailed you want the explanation to be"
        )
    
    # Action button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📚 Explain Topic", type="primary", use_container_width=True):
            if topic:
                with st.spinner("🔍 Analyzing topic and preparing explanation..."):
                    try:
                        # Get relevant content
                        context = st.session_state.knowledge_base.get_relevant_content(
                            topic, subject, class_level
                        )
                        
                        # Generate explanation
                        explanation = st.session_state.gemini_client.explain_topic(
                            topic, context, subject, class_level, explanation_type
                        )
                        
                        st.success(f"✅ {explanation_type} explanation generated!")
                        
                        # Enhanced explanation display
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1a1a1a, #2a2a2a); padding: 2rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid #00b4ff;">
                            <h3 style="color: #00b4ff; margin-bottom: 1rem;">📚 {explanation_type} Explanation: {topic}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(explanation)
                        
                        # Additional learning options
                        st.markdown("---")
                        st.markdown("### 🚀 Continue Learning")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("❓ Ask Question", key="topic_ask"):
                                st.info("Switch to 'Ask Doubts' to ask specific questions about this topic!")
                        with col2:
                            if st.button("📝 Generate Quiz", key="topic_quiz"):
                                st.info("Switch to 'Generate Quiz' to test your understanding!")
                        with col3:
                            if st.button("🔄 Related Topics", key="topic_related"):
                                st.info("Ask for related topics in the question section!")
                        
                    except Exception as e:
                        st.error(f"❌ Error generating explanation: {str(e)}")
                        st.info("💡 Try checking your internet connection or rephrasing the topic.")
            else:
                st.warning("⚠️ Please enter a topic name to get started!")

elif feature == "Generate Quiz":
    # Feature header with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2a2a2a, #1a1a1a); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #333;">
        <h2 style="color: #ffc107; margin-bottom: 0.5rem; display: flex; align-items: center;">
            📝 Quiz Generator
        </h2>
        <p style="color: #b0b0b0; margin: 0; font-size: 1.1rem;">
            Test your knowledge with personalized AI-generated quizzes based on NCERT curriculum
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Quiz Configuration")
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
    # Feature header with enhanced styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2a2a2a, #1a1a1a); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border: 1px solid #333;">
        <h2 style="color: #ff6b7a; margin-bottom: 0.5rem; display: flex; align-items: center;">
            📝 Homework Helper
        </h2>
        <p style="color: #b0b0b0; margin: 0; font-size: 1.1rem;">
            Get intelligent, step-by-step assistance with your homework problems
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📖 Enter Your Problem")
        problem = st.text_area(
            "Homework problem:",
            placeholder="e.g., Solve: 2x + 5 = 15\nFind the area of a triangle with base 8cm and height 6cm\nExplain the causes of World War I",
            height=150,
            help="Enter your homework question or problem statement"
        )
    
    with col2:
        st.markdown("### 🎯 Help Type")
        help_type = st.selectbox(
            "What kind of help do you need?",
            ["Step-by-step solution", "Concept explanation", "Hint only", "Similar examples"],
            help="Choose the type of assistance you prefer"
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

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a, #0f0f0f); padding: 3rem 2rem; border-radius: 12px; margin-top: 3rem; border: 1px solid #333; text-align: center;">
    <div style="margin-bottom: 2rem;">
        <h3 style="color: #00ff88; margin-bottom: 1rem; font-size: 1.5rem;">🎓 AI Tutor for Indian Students</h3>
        <p style="color: #b0b0b0; font-size: 1.1rem; margin: 0;">Empowering education through artificial intelligence</p>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem; flex-wrap: wrap;">
        <div style="color: #00ff88;">
            <strong>🤖 Powered by</strong><br>
            <span style="color: #b0b0b0;">Gemini AI</span>
        </div>
        <div style="color: #00b4ff;">
            <strong>📚 Curriculum</strong><br>
            <span style="color: #b0b0b0;">NCERT Based</span>
        </div>
        <div style="color: #ffc107;">
            <strong>🎯 Coverage</strong><br>
            <span style="color: #b0b0b0;">Classes 6-12</span>
        </div>
        <div style="color: #ff6b7a;">
            <strong>📖 Subjects</strong><br>
            <span style="color: #b0b0b0;">All Major Subjects</span>
        </div>
    </div>
    
    <div style="border-top: 1px solid #333; padding-top: 1.5rem;">
        <p style="color: #888; font-size: 0.9rem; margin: 0;">
            <em>Making quality education accessible to all Indian students</em>
        </p>
        <p style="color: #666; font-size: 0.8rem; margin-top: 0.5rem;">
            Built with ❤️ for the future of education in India
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
