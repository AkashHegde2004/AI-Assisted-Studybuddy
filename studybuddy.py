import streamlit as st
import json
import re
from groq import Groq
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="StudyBuddy - AI Learning Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #1f77b4, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        animation: gradient 3s ease-in-out infinite;
    }

    @keyframes gradient {
        0%, 100% { filter: hue-rotate(0deg); }
        50% { filter: hue-rotate(90deg); }
    }

    .nav-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 5px;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-decoration: none;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .home-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }

    .home-card:hover {
        transform: translateY(-5px);
    }

    .feature-card {
        background: black
    ;
        padding: 25px;
        border-radius: 15px;
        margin: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        transition: all 0.3s ease;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }

    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 2rem 0;
        padding: 15px;
        background: linear-gradient(90deg, #e3f2fd, #ffffff);
        border-left: 5px solid #1f77b4;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .quiz-question {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #dee2e6;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .quiz-question:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .correct-answer {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border: 2px solid #28a745;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: pulse 2s infinite;
    }

    .incorrect-answer {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border: 2px solid #dc3545;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: shake 0.5s;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    .score-display {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        animation: bounceIn 1s;
    }

    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }

    .excellent-score {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border: 3px solid #28a745;
    }

    .good-score {
        background: linear-gradient(135deg, #d1ecf1, #bee5eb);
        color: #0c5460;
        border: 3px solid #17a2b8;
    }

    .average-score {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        color: #856404;
        border: 3px solid #ffc107;
    }

    .poor-score {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border: 3px solid #dc3545;
    }

    .sidebar-info {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .study-content {
        background: white;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #dee2e6;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .study-content:hover {
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }

    .ai-chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }

    .chat-message {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }

    .floating-emoji {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .progress-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 8px;
        border-radius: 4px;
        margin: 10px 0;
        animation: progress 2s ease-in-out;
    }

    @keyframes progress {
        0% { width: 0%; }
        100% { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'groq_client' not in st.session_state:
        st.session_state.groq_client = None
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'study_content' not in st.session_state:
        st.session_state.study_content = ""
    if 'quiz_results' not in st.session_state:
        st.session_state.quiz_results = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'study_progress' not in st.session_state:
        st.session_state.study_progress = {'topics_studied': 0, 'quizzes_taken': 0, 'total_score': 0}

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

# Initialize Groq client
def init_groq_client(api_key):
    try:
        client = Groq(api_key=api_key)
        st.session_state.groq_client = client
        return True
    except Exception as e:
        st.error(f"Error initializing Groq client: {str(e)}")
        return False

# Generate study content using Groq
def generate_study_content(topic, difficulty_level, content_type):
    if not st.session_state.groq_client:
        st.error("Please enter your Groq API key first!")
        return ""

    try:
        prompt = f"""
        Create comprehensive study material about {topic} for {difficulty_level} level students.
        Content type: {content_type}

        Please provide:
        1. Clear explanation of key concepts
        2. Important definitions with examples
        3. Real-world applications and examples
        4. Key points to remember
        5. Practice tips

        Make it engaging, educational, and well-structured with proper headings.
        """

        response = st.session_state.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert educator who creates clear, comprehensive, and engaging study materials with proper formatting."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=2500,
        )

        # Update progress
        st.session_state.study_progress['topics_studied'] += 1

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating study content: {str(e)}")
        return ""

# Generate quiz questions using Groq
def generate_quiz_questions(topic, difficulty_level, num_questions):
    if not st.session_state.groq_client:
        st.error("Please enter your Groq API key first!")
        return []

    try:
        prompt = f"""
        Create {num_questions} multiple choice questions about {topic} for {difficulty_level} level students.

        Format each question as JSON with this exact structure:
        {{
            "question": "Question text here",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A",
            "explanation": "Detailed explanation of why this answer is correct and why others are wrong"
        }}

        Make questions challenging but fair. Ensure good variety in question types.
        Return only a JSON array of questions, no additional text.
        """

        response = st.session_state.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert quiz creator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=2500,
        )

        content = response.choices[0].message.content.strip()

        # Clean up the response to extract JSON
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]

        questions = json.loads(content)
        return questions
    except Exception as e:
        st.error(f"Error generating quiz questions: {str(e)}")
        return []

# AI Assistant function
def get_ai_response(question, context=""):
    if not st.session_state.groq_client:
        return "Please enter your Groq API key first!"

    try:
        context_prompt = f"Context: {context}\n\n" if context else ""
        prompt = f"{context_prompt}Question: {question}\n\nPlease provide a helpful, clear, and educational response."

        response = st.session_state.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI tutor. Provide clear, educational responses with examples when appropriate."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1500,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting AI response: {str(e)}"

# Grade quiz and provide feedback
def grade_quiz():
    if not st.session_state.quiz_questions:
        st.error("No quiz questions available!")
        return

    correct_answers = 0
    total_questions = len(st.session_state.quiz_questions)
    results = {}

    for i, question in enumerate(st.session_state.quiz_questions):
        user_answer = st.session_state.quiz_answers.get(f"q_{i}", "")
        correct_answer = question["correct_answer"]

        is_correct = user_answer == correct_answer
        if is_correct:
            correct_answers += 1

        results[i] = {
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question["explanation"]
        }

    score_percentage = (correct_answers / total_questions) * 100

    # Update progress
    st.session_state.study_progress['quizzes_taken'] += 1
    st.session_state.study_progress['total_score'] += score_percentage

    st.session_state.quiz_results = {
        "score": score_percentage,
        "correct": correct_answers,
        "total": total_questions,
        "results": results
    }

    st.session_state.quiz_submitted = True

# Create progress visualization
def create_progress_chart():
    progress = st.session_state.study_progress

    if progress['quizzes_taken'] > 0:
        avg_score = progress['total_score'] / progress['quizzes_taken']

        # Create a gauge chart for average score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = avg_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Average Quiz Score"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
        

        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        return fig
    return None

# Create study statistics
def create_study_stats():
    progress = st.session_state.study_progress

    data = {
        'Metric': ['Topics Studied', 'Quizzes Taken', 'Avg Score'],
        'Value': [
            progress['topics_studied'],
            progress['quizzes_taken'],
            round(progress['total_score'] / max(progress['quizzes_taken'], 1), 1)
        ]
    }

    fig = px.bar(
        data,
        x='Metric',
        y='Value',
        title="Your Learning Journey",
        color='Value',
        color_continuous_scale='viridis'
    )

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# Home page
def show_home_page():
    st.markdown('<h1 class="main-header">🎓 Welcome to StudyBuddy!</h1>', unsafe_allow_html=True)

    # Fun animated emojis
    cols = st.columns(5)
    emojis = ["📚", "🧠", "🎯", "🚀", "⭐"]
    for i, (col, emoji) in enumerate(zip(cols, emojis)):
        with col:
            st.markdown(f'<div class="floating-emoji" style="animation-delay: {i*0.2}s;">{emoji}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="home-card">
        <h2>🌟 Your AI-Powered Learning Companion</h2>
        <p>Transform your learning experience with personalized study materials, interactive quizzes, and intelligent assistance!</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📚 Study Materials", key="nav_study_1", help="Generate AI-powered study content"):
            navigate_to('study')
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Smart Study Materials</h3>
            <p>Get personalized study content tailored to your level and learning style</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🧠 Interactive Quiz", key="nav_quiz_1", help="Test your knowledge with AI-generated quizzes"):
            navigate_to('quiz')
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Smart Quizzes</h3>
            <p>Challenge yourself with AI-generated questions and instant feedback</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("🤖 AI Assistant", key="nav_assistant_1", help="Chat with your AI tutor"):
            navigate_to('assistant')
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Tutor</h3>
            <p>Get instant help and explanations from your personal AI assistant</p>
        </div>
        """, unsafe_allow_html=True)

    # Progress visualization
    if st.session_state.study_progress['topics_studied'] > 0 or st.session_state.study_progress['quizzes_taken'] > 0:
        st.markdown('<h2 class="section-header">📊 Your Learning Progress</h2>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            progress_chart = create_progress_chart()
            if progress_chart:
                st.plotly_chart(progress_chart, use_container_width=True)

        with col2:
            stats_chart = create_study_stats()
            st.plotly_chart(stats_chart, use_container_width=True)

# Study materials page
def show_study_page():
    st.markdown('<h1 class="section-header">📚 AI-Generated Study Materials</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        topic = st.text_input("🎯 Study Topic:", placeholder="e.g., Python Programming, World War II, Calculus", key="study_topic")

    with col2:
        if st.button("🚀 Generate Content", type="primary", key="generate_content", use_container_width=True):
            if topic:
                with st.spinner("🧠 AI is creating your personalized study materials..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)

                    content = generate_study_content(
                        topic,
                        st.session_state.get('difficulty_level', 'Intermediate'),
                        st.session_state.get('content_type', 'Comprehensive Overview')
                    )
                    st.session_state.study_content = content
                    st.balloons()
            else:
                st.warning("⚠️ Please enter a study topic first!")

    if st.session_state.study_content:
        st.markdown('<div class="study-content">', unsafe_allow_html=True)
        st.markdown(st.session_state.study_content)
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Study Notes",
                data=st.session_state.study_content,
                file_name=f"study_notes_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                key="download_notes",
                use_container_width=True
            )

        with col2:
            if st.button("🧠 Generate Quiz on This Topic", key="generate_quiz_from_study", use_container_width=True):
                navigate_to('quiz')

# Quiz page
def show_quiz_page():
    st.markdown('<h1 class="section-header">🧠 Interactive Quiz & Assessment</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        topic = st.text_input("🎯 Quiz Topic:", key="quiz_topic")

    with col2:
        num_questions = st.selectbox("❓ Number of Questions:", [3, 5, 7, 10], index=1, key="num_questions")

    with col3:
        if st.button("🎯 Generate Quiz", type="primary", key="generate_quiz", use_container_width=True):
            if topic:
                with st.spinner("🎲 Creating your personalized quiz..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)

                    questions = generate_quiz_questions(
                        topic,
                        st.session_state.get('difficulty_level', 'Intermediate'),
                        num_questions
                    )
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_results = {}
                    st.success("✅ Quiz generated successfully!")
            else:
                st.warning("⚠️ Please enter a quiz topic first!")

    # Display quiz questions
    if st.session_state.quiz_questions and not st.session_state.quiz_submitted:
        st.markdown("### 🎲 Answer the following questions:")

        for i, question in enumerate(st.session_state.quiz_questions):
            st.markdown(f'<div class="quiz-question">', unsafe_allow_html=True)
            st.markdown(f"**Question {i+1}:** {question['question']}")

            answer = st.radio(
                f"Select your answer for Question {i+1}:",
                question["options"],
                key=f"q_{i}",
                label_visibility="collapsed"
            )

            if answer:
                st.session_state.quiz_answers[f"q_{i}"] = answer[0]

            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("📊 Submit Quiz", type="secondary", key="submit_quiz", use_container_width=True):
            grade_quiz()
            st.balloons()

    # Display quiz results
    if st.session_state.quiz_submitted and st.session_state.quiz_results:
        results = st.session_state.quiz_results
        score = results["score"]

        # Score display with animations
        if score >= 90:
            score_class = "excellent-score"
            emoji = "🏆"
            message = "Excellent Work!"
        elif score >= 75:
            score_class = "good-score"
            emoji = "👍"
            message = "Great Job!"
        elif score >= 60:
            score_class = "average-score"
            emoji = "📚"
            message = "Keep Studying!"
        else:
            score_class = "poor-score"
            emoji = "💪"
            message = "Practice Makes Perfect!"

        st.markdown(f'''
        <div class="score-display {score_class}">
            {emoji} {message}<br>
            Score: {results["correct"]}/{results["total"]} ({score:.1f}%)
        </div>
        ''', unsafe_allow_html=True)

        # Detailed results
        st.markdown("### 📋 Detailed Results:")

        for i, result in results["results"].items():
            if result["is_correct"]:
                st.markdown(f'<div class="correct-answer">', unsafe_allow_html=True)
                st.markdown(f"**Question {i+1}:** ✅ Correct!")
            else:
                st.markdown(f'<div class="incorrect-answer">', unsafe_allow_html=True)
                st.markdown(f"**Question {i+1}:** ❌ Incorrect")
                st.markdown(f"**Your answer:** {result['user_answer']}")
                st.markdown(f"**Correct answer:** {result['correct_answer']}")

            st.markdown(f"**Question:** {result['question']}")
            st.markdown(f"**💡 Explanation:** {result['explanation']}")
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Take New Quiz", key="new_quiz", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_results = {}
                st.rerun()

        with col2:
            if st.button("🤖 Ask AI for Help", key="ask_ai_help", use_container_width=True):
                navigate_to('assistant')

# AI Assistant page
def show_assistant_page():
    st.markdown('<h1 class="section-header">🤖 AI Learning Assistant</h1>', unsafe_allow_html=True)

    if not st.session_state.groq_client:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to use the AI assistant!")
        return

    st.markdown("""
    <div class="ai-chat-container">
        <h3>💬 Chat with your AI Tutor</h3>
        <p>Ask questions, get explanations, or seek help with any topic!</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick help buttons
    st.markdown("### 🚀 Quick Help:")
    col1, col2, col3, col4 = st.columns(4)

    quick_questions = [
        "Explain this concept simply",
        "Give me practice problems",
        "What are the key points?",
        "How can I remember this?"
    ]

    for i, (col, question) in enumerate(zip([col1, col2, col3, col4], quick_questions)):
        with col:
            if st.button(question, key=f"quick_{i}"):
                st.session_state.chat_input = question

    # Chat interface
    user_question = st.text_area("💭 Ask your question:", height=100, key="chat_input")

    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("📤 Send", type="primary", key="send_button")

    if send_button and user_question:
        with st.spinner("🤔 AI is thinking..."):
            # Add context from recent study materials or quiz
            context = ""
            if st.session_state.study_content:
                context += f"Recent study material: {st.session_state.study_content[:500]}..."

            response = get_ai_response(user_question, context)

            # Add to chat history
            st.session_state.chat_history.append({
                "question": user_question,
                "response": response,
                "timestamp": datetime.now().strftime("%H:%M")
            })

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Chat History:")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5 chats
            st.markdown(f'<div class="chat-message">', unsafe_allow_html=True)
            st.markdown(f"**🙋 You ({chat['timestamp']}):** {chat['question']}")
            st.markdown(f"**🤖 AI Tutor:** {chat['response']}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

# Sidebar setup
def setup_sidebar():
    with st.sidebar:
        # Navigation
        st.markdown('<div class="sidebar-info"><h3>🧭 Navigation</h3></div>', unsafe_allow_html=True)

        nav_buttons = [
            ("🏠 Home", "home"),
            ("📚 Study Materials", "study"),
            ("🧠 Quiz & Test", "quiz"),
            ("🤖 AI Assistant", "assistant")
        ]

        for label, page in nav_buttons:
            if st.button(label, key=f"nav_{page}_sidebar", use_container_width=True):
                navigate_to(page)

        st.markdown("---")

        # API Configuration
        st.markdown('<div class="sidebar-info"><h3>🔑 API Configuration</h3></div>', unsafe_allow_html=True)

        groq_api_key = st.text_input(
            "Enter your Groq API Key:",
            type="password",
            help="Get your free API key from https://console.groq.com/keys",
            key="groq_api_key"
        )

        if groq_api_key:
            if init_groq_client(groq_api_key):
                st.success("✅ Connected!")
            else:
                st.error("❌ Invalid Key")

        st.markdown("---")

        # Study Settings
        st.markdown('<div class="sidebar-info"><h3>⚙️ Study Settings</h3></div>', unsafe_allow_html=True)

        difficulty_level = st.selectbox(
            "🎚️ Difficulty Level:",
            ["Beginner", "Intermediate", "Advanced"],
            key="difficulty_level_sidebar"
        )

        content_type = st.selectbox(
            "📝 Content Type:",
            ["Comprehensive Overview", "Key Concepts", "Practice Problems", "Summary Notes"],
            key="content_type_sidebar"
        )

        st.markdown("---")

        # Progress Overview
        if st.session_state.study_progress['topics_studied'] > 0 or st.session_state.study_progress['quizzes_taken'] > 0:
            st.markdown('<div class="sidebar-info"><h3>📈 Your Progress</h3></div>', unsafe_allow_html=True)

            progress = st.session_state.study_progress

            st.metric("📚 Topics Studied", progress['topics_studied'])
            st.metric("🧠 Quizzes Taken", progress['quizzes_taken'])

            if progress['quizzes_taken'] > 0:
                avg_score = progress['total_score'] / progress['quizzes_taken']
                st.metric("⭐ Average Score", f"{avg_score:.1f}%")

        st.markdown("---")

        # Fun facts
        st.markdown('<div class="sidebar-info"><h3>💡 Study Tip</h3></div>', unsafe_allow_html=True)

        study_tips = [
            "Take breaks every 25 minutes (Pomodoro Technique)! 🍅",
            "Teaching others helps you learn better! 👥",
            "Practice testing improves memory retention! 🧠",
            "Sleep is crucial for memory consolidation! 😴",
            "Exercise boosts cognitive function! 🏃‍♂️",
            "Use multiple senses while studying! 👁️👂",
            "Spaced repetition is more effective than cramming! ⏰"
        ]

        tip_index = (datetime.now().day) % len(study_tips)
        st.info(study_tips[tip_index])

# Main app function
def main():
    initialize_session_state()
    setup_sidebar()

    # Main content based on current page
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'study':
        show_study_page()
    elif st.session_state.current_page == 'quiz':
        show_quiz_page()
    elif st.session_state.current_page == 'assistant':
        show_assistant_page()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🎓 StudyBuddy - Powered by AI | Made with ❤️ using Streamlit & Groq</p>
        <p>💡 <em>Learning is a journey, not a destination!</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
