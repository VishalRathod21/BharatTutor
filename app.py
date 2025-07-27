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
    page_title="Bharat Tutor",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Modern header with improved design
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem; padding: 3rem 2rem; background: linear-gradient(135deg, #111111, #000000); border-radius: 20px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.1);">
    <div style="font-size: 4rem; margin-bottom: 1rem;">🇮🇳</div>
    <h1 style="color: #00ff88; font-size: 3rem; font-weight: 800; margin-bottom: 1rem; text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);">Bharat Tutor</h1>
    <p style="font-size: 1.3rem; color: #bbbbbb; font-weight: 300; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
        Your intelligent NCERT curriculum assistant powered by advanced AI technology
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        <span style="background: linear-gradient(45deg, #00ff88, #00b4ff); color: #000; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">AI Powered</span>
        <span style="background: linear-gradient(45deg, #00b4ff, #ffc107); color: #000; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">NCERT Based</span>
        <span style="background: linear-gradient(45deg, #ffc107, #ff6b7a); color: #000; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600;">Classes 6-12</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Modern sidebar with enhanced design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem; padding: 2rem 1rem; background: linear-gradient(135deg, #111111, #222222); border-radius: 15px; border: 1px solid #333;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🇮🇳</div>
        <h2 style="color: #00ff88; margin-bottom: 0.5rem; font-size: 1.3rem; font-weight: 700;">Bharat Tutor</h2>
        <p style="color: #bbbbbb; font-size: 0.9rem; margin: 0;">AI Learning Assistant</p>
        <div style="width: 60px; height: 3px; background: linear-gradient(45deg, #00ff88, #00b4ff); margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature selection with modern cards
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h3 style="color: #00ff88; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">🚀 Learning Mode</h3>
    </div>
    """, unsafe_allow_html=True)
    
    feature = st.selectbox(
        "Select Learning Mode",
        ["Ask Doubts", "Explain Topic", "Generate Quiz", "Homework Helper"],
        help="Choose what you'd like to do today",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Academic settings with better layout
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #00b4ff; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">📚 Study Settings</h3>
    </div>
    """, unsafe_allow_html=True)
    
    class_level = st.selectbox(
        "Class Level:",
        ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"],
        help="Select your current class"
    )
    
    subject = st.selectbox(
        "Subject:",
        ["Mathematics", "Science", "Social Science", "English", "Hindi"],
        help="Choose the subject you need help with"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick actions with modern styling
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #ffc107; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">⚡ Quick Actions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History", help="Clear conversation history", use_container_width=True):
        st.session_state.conversation_memory.clear()
        st.success("History cleared!")
        st.rerun()
    
    if st.button("📊 View Stats", help="View learning statistics", use_container_width=True):
        stats = st.session_state.conversation_memory.get_statistics()
        if stats['total_conversations'] > 0:
            st.json(stats)
        else:
            st.info("No conversations yet!")
    
    # Progress section with metrics
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #ff6b7a; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">📈 Your Progress</h3>
    </div>
    """, unsafe_allow_html=True)
    
    total_conversations = len(st.session_state.conversation_memory.get_history())
    if total_conversations > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Questions", total_conversations, delta=None)
        
        with col2:
            stats = st.session_state.conversation_memory.get_statistics()
            if 'subjects_used' in stats:
                most_active = stats.get('most_active_subject', 'None')
                if len(most_active) > 8:
                    most_active = most_active[:8] + "..."
                st.metric("Top Subject", most_active)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: #111111; border-radius: 10px; border: 1px solid #333;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌟</div>
            <p style="color: #bbbbbb; margin: 0; font-size: 0.9rem;">Start learning to track progress!</p>
        </div>
        """, unsafe_allow_html=True)

# Main content area with modern styling
if feature == "Ask Doubts":
    # Modern feature header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; border: 1px solid #333; box-shadow: 0 8px 25px rgba(0, 255, 136, 0.1);">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">❓</div>
            <h2 style="color: #00ff88; margin: 0; font-size: 2rem; font-weight: 700;">Ask Your Doubts</h2>
        </div>
        <p style="color: #bbbbbb; margin: 0; font-size: 1.2rem; line-height: 1.6;">
            Get instant, detailed explanations for any question from your NCERT syllabus with AI-powered assistance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create modern tabs for better organization
    tab1, tab2 = st.tabs(["💬 Ask Question", "📚 Conversation History"])
    
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
                            <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #00ff88; box-shadow: 0 5px 15px rgba(0, 255, 136, 0.1);">
                                <h3 style="color: #00ff88; margin-bottom: 1.5rem; font-size: 1.4rem; font-weight: 600;">💡 Your Answer</h3>
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
    # Modern feature header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; border: 1px solid #333; box-shadow: 0 8px 25px rgba(0, 180, 255, 0.1);">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">📖</div>
            <h2 style="color: #00b4ff; margin: 0; font-size: 2rem; font-weight: 700;">Topic Explanation</h2>
        </div>
        <p style="color: #bbbbbb; margin: 0; font-size: 1.2rem; line-height: 1.6;">
            Get comprehensive explanations for any chapter or topic from your NCERT curriculum with detailed insights
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
                        <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 15px; margin: 1.5rem 0; border-left: 5px solid #00b4ff; box-shadow: 0 5px 15px rgba(0, 180, 255, 0.1);">
                            <h3 style="color: #00b4ff; margin-bottom: 1.5rem; font-size: 1.4rem; font-weight: 600;">📚 {explanation_type} Explanation: {topic}</h3>
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
    # Modern feature header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; border: 1px solid #333; box-shadow: 0 8px 25px rgba(255, 193, 7, 0.1);">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">📝</div>
            <h2 style="color: #ffc107; margin: 0; font-size: 2rem; font-weight: 700;">Quiz Generator</h2>
        </div>
        <p style="color: #bbbbbb; margin: 0; font-size: 1.2rem; line-height: 1.6;">
            Test your knowledge with personalized AI-generated quizzes based on NCERT curriculum standards
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
    # Modern feature header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2.5rem; border-radius: 20px; margin-bottom: 2rem; border: 1px solid #333; box-shadow: 0 8px 25px rgba(255, 107, 122, 0.1);">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">🎯</div>
            <h2 style="color: #ff6b7a; margin: 0; font-size: 2rem; font-weight: 700;">Homework Helper</h2>
        </div>
        <p style="color: #bbbbbb; margin: 0; font-size: 1.2rem; line-height: 1.6;">
            Get intelligent, step-by-step assistance with your homework problems and assignments
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

# Modern Footer
st.markdown("---")

with st.container():
    # Main footer header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 3rem 2rem; border-radius: 20px; margin-top: 3rem; border: 1px solid #333; text-align: center; box-shadow: 0 10px 30px rgba(0, 255, 136, 0.05);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🇮🇳</div>
        <h3 style="color: #00ff88; font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">Bharat Tutor</h3>
        <p style="color: #bbbbbb; font-size: 1.2rem; margin-bottom: 2rem;">Empowering education through artificial intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature highlights using columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #111111, #000000); border-radius: 15px; border: 1px solid #333; box-shadow: 0 5px 15px rgba(0, 255, 136, 0.1);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🤖</div>
            <div style="color: #00ff88; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">AI Powered</div>
            <div style="color: #bbbbbb; font-size: 0.9rem;">Gemini AI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #111111, #000000); border-radius: 15px; border: 1px solid #333; box-shadow: 0 5px 15px rgba(0, 180, 255, 0.1);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📚</div>
            <div style="color: #00b4ff; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Curriculum</div>
            <div style="color: #bbbbbb; font-size: 0.9rem;">NCERT Based</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #111111, #000000); border-radius: 15px; border: 1px solid #333; box-shadow: 0 5px 15px rgba(255, 193, 7, 0.1);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
            <div style="color: #ffc107; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Coverage</div>
            <div style="color: #bbbbbb; font-size: 0.9rem;">Classes 6-12</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 1rem; background: linear-gradient(135deg, #111111, #000000); border-radius: 15px; border: 1px solid #333; box-shadow: 0 5px 15px rgba(255, 107, 122, 0.1);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">📖</div>
            <div style="color: #ff6b7a; font-weight: 700; margin-bottom: 0.5rem; font-size: 1rem;">Subjects</div>
            <div style="color: #bbbbbb; font-size: 0.9rem;">All Major</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Final message with modern styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #111111, #000000); padding: 2rem; border-radius: 15px; margin-top: 2rem; border: 1px solid #333; text-align: center; box-shadow: 0 5px 15px rgba(0, 255, 136, 0.05);">
        <p style="color: #bbbbbb; font-size: 1rem; margin: 0; margin-bottom: 0.5rem;">
            <em>Making quality education accessible to all Indian students</em>
        </p>
        <p style="color: #888888; font-size: 0.9rem; margin: 0;">
            Built with ❤️ for the future of education in India
        </p>
    </div>
    """, unsafe_allow_html=True)
