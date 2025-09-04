# app.py - Streamlit Frontend
import streamlit as st
import requests
import json
from typing import Dict

# Configure page
st.set_page_config(
    page_title="Equanimity: Path to Inner Balance",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Buddhist aesthetic
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
    
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f5f3f0 0%, #e8e4df 100%);
        font-family: 'Crimson Text', serif;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .lotus-symbol {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(139, 69, 19, 0.3));
    }
    
    .main-title {
        font-size: 3.5rem;
        color: #5D4E37;
        font-weight: 300;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.4rem;
        color: #7B6143;
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    /* Content card styling */
    .content-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(139, 69, 19, 0.15);
        border: 1px solid rgba(139, 69, 19, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Question styling */
    .question-container {
        background: rgba(245, 243, 240, 0.8);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 4px solid #8B4513;
    }
    
    .question-number {
        font-size: 1rem;
        color: #8B4513;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .question-text {
        font-size: 1.5rem;
        color: #5D4E37;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    /* Option styling */
    .option-card {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(139, 69, 19, 0.2);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .option-card:hover {
        border-color: rgba(139, 69, 19, 0.5);
        box-shadow: 0 4px 15px rgba(139, 69, 19, 0.2);
        transform: translateY(-2px);
    }
    
    .option-title {
        font-weight: 600;
        color: #5D4E37;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .option-keywords {
        color: #8B4513;
        font-size: 1rem;
        font-style: italic;
    }
    
    /* Zen quote styling */
    .zen-quote {
        font-style: italic;
        color: #7B6143;
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(139, 69, 19, 0.08);
        border-left: 4px solid #8B4513;
        border-radius: 8px;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    /* Results styling */
    .technique-title {
        font-size: 2.2rem;
        color: #5D4E37;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .technique-description {
        font-size: 1.2rem;
        color: #6B5B47;
        line-height: 1.7;
        margin-bottom: 2rem;
    }
    
    .day-section {
        background: rgba(139, 69, 19, 0.1);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 4px solid #8B4513;
    }
    
    .day-title {
        font-size: 1.6rem;
        color: #5D4E37;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    .practice-section {
        margin-bottom: 1.5rem;
    }
    
    .practice-label {
        font-weight: 600;
        color: #8B4513;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .practice-content {
        color: #6B5B47;
        line-height: 1.6;
        font-size: 1.05rem;
    }
    
    /* Progress bar */
    .progress-container {
        background: rgba(139, 69, 19, 0.2);
        border-radius: 10px;
        height: 12px;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #8B4513, #A0522D);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        font-family: 'Crimson Text', serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 69, 19, 0.4);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Radio button styling */
    .stRadio > div {
        gap: 1rem;
    }
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"  # Change this for production

# Questions data
QUESTIONS = [
    {
        "number": 1,
        "text": "When facing unexpected challenges or setbacks, what is your most natural response?",
        "options": [
            ("I feel immediately overwhelmed and react strongly", "reactive, overwhelming, scattered, intense, turbulent"),
            ("I become anxious and worry about outcomes", "anxious, worried, uncertain, restless, concerned"),
            ("I pause to analyze and plan my response", "analyzing, planning, methodical, logical, structured"),
            ("I accept what is and adapt with minimal resistance", "accepting, flowing, adaptable, resilient, balanced")
        ]
    },
    {
        "number": 2,
        "text": "How do you typically respond to criticism or negative feedback from others?",
        "options": [
            ("I feel hurt and become defensive", "defensive, hurt, rejected, wounded, protective"),
            ("I ruminate and question my self-worth", "ruminating, doubting, questioning, insecure, overthinking"),
            ("I evaluate if there's truth to consider", "evaluating, discerning, selective, rational, measured"),
            ("I receive it as information for growth", "grateful, learning, growing, open, receptive")
        ]
    },
    {
        "number": 3,
        "text": "When experiencing intense emotions (anger, sadness, fear), what best describes your relationship with them?",
        "options": [
            ("I become completely consumed by the emotion", "consumed, identified, merged, lost, overwhelmed"),
            ("I try to suppress or avoid the feeling", "suppressing, avoiding, numbing, escaping, denying"),
            ("I work through it with effort and understanding", "understanding, processing, working, healing, therapeutic"),
            ("I observe it with spacious awareness", "witnessing, observing, spacious, present, aware")
        ]
    },
    {
        "number": 4,
        "text": "How do you approach situations where you cannot control the outcome?",
        "options": [
            ("I fight harder to maintain control", "fighting, forcing, pushing, struggling, resisting"),
            ("I feel frustrated and helpless", "frustrated, helpless, powerless, defeated, stuck"),
            ("I focus on what I can influence", "focusing, manageable, practical, actionable, organized"),
            ("I surrender to the flow of life", "surrendering, trusting, releasing, peaceful, flowing")
        ]
    },
    {
        "number": 5,
        "text": "What is your relationship with pleasure and success versus pain and failure?",
        "options": [
            ("I cling to pleasure and desperately avoid pain", "clinging, addicted, desperate, dependent, attached"),
            ("I swing between highs and lows dramatically", "swinging, unstable, moody, reactive, volatile"),
            ("I try to maintain balance through discipline", "moderating, balancing, managing, controlled, disciplined"),
            ("I remain relatively unchanged by either", "equanimous, steady, unchanged, centered, stable")
        ]
    }
]

def render_header():
    """Render the beautiful header with lotus symbol"""
    st.markdown("""
    <div class="header-container">
        <div class="lotus-symbol">🪷</div>
        <h1 class="main-title">Equanimity</h1>
        <p class="subtitle">Path to Inner Balance & Peaceful Awareness</p>
    </div>
    """, unsafe_allow_html=True)

def render_intro():
    """Render the introduction section"""
    st.markdown("""
    <div class="content-card">
        <h2 style="color: #5D4E37; text-align: center; font-size: 2.2rem; margin-bottom: 2rem;">Understanding Equanimity</h2>
        
        <p style="font-size: 1.2rem; line-height: 1.7; color: #6B5B47; margin-bottom: 1.5rem;">
        Equanimity is one of Buddhism's most profound teachings—a state of mental calmness and composure, especially in difficult situations. It represents balanced awareness, neither grasping at pleasant experiences nor pushing away unpleasant ones.
        </p>
        
        <div class="zen-quote">
            "In the midst of winter, I found there was, within me, an invincible summer." - Albert Camus
        </div>
        
        <p style="font-size: 1.2rem; line-height: 1.7; color: #6B5B47; margin-bottom: 1.5rem;">
        This quality of mind allows us to remain centered and wise regardless of external circumstances. Equanimity isn't indifference—it's engaged peace, responding to life with clarity rather than reactivity.
        </p>
        
        <p style="font-size: 1.2rem; line-height: 1.7; color: #6B5B47; margin-bottom: 2rem;">
        <strong>Why Equanimity Matters:</strong> It frees us from the exhausting cycle of emotional highs and lows, reduces suffering caused by attachment and aversion, and enables clearer decision-making and deeper compassion.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_question(question_data, question_key):
    """Render a single question with options"""
    st.markdown(f"""
    <div class="question-container">
        <div class="question-number">QUESTION {question_data['number']} OF 5</div>
        <div class="question-text">{question_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create radio button options
    option_labels = [opt[0] for opt in question_data['options']]
    
    selected = st.radio(
        "",
        option_labels,
        key=question_key,
        label_visibility="collapsed"
    )
    
    # Display selected option with keywords
    if selected:
        for option_text, keywords in question_data['options']:
            if option_text == selected:
                st.markdown(f"""
                <div style="background: rgba(139, 69, 19, 0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                    <strong style="color: #5D4E37;">Selected:</strong> {option_text}<br>
                    <em style="color: #8B4513;">Keywords: {keywords}</em>
                </div>
                """, unsafe_allow_html=True)
                return keywords
    
    return None

def render_progress_bar(current_question, total_questions):
    """Render progress bar"""
    progress = (current_question - 1) / total_questions * 100
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%;"></div>
    </div>
    <p style="text-align: center; color: #8B4513; font-weight: 500;">
        Progress: {current_question - 1} of {total_questions} questions completed
    </p>
    """, unsafe_allow_html=True)

def call_api(answers: Dict[str, str]):
    """Call the FastAPI backend to generate technique"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-technique",
            json={"answers": answers},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Error**: Cannot connect to the API server. Please ensure the FastAPI server is running on http://localhost:8000")
        st.info("💡 **To start the server**: Run `uvicorn main:app --reload` in your terminal")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ **Timeout Error**: The AI is taking longer than expected. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 **API Error**: {str(e)}")
        return None

def render_technique(technique_data):
    """Render the generated technique"""
    st.markdown(f"""
    <div class="content-card">
        <h2 class="technique-title">{technique_data['technique_title']}</h2>
        <div class="technique-description">
            <p>{technique_data['description']}</p>
        </div>
        
        <div class="zen-quote">
            "{technique_data['zen_quote']}"
        </div>
        
        <div style="background: rgba(139, 69, 19, 0.08); padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
            <strong style="color: #5D4E37; font-size: 1.1rem;">Key Insight:</strong>
            <p style="margin-top: 0.5rem; font-style: italic; color: #6B5B47;">{technique_data['insight']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render each day
    for day_num in [1, 2, 3]:
        day_data = technique_data[f'day{day_num}']
        st.markdown(f"""
        <div class="day-section">
            <div class="day-title">Day {day_num}: {day_data['title']}</div>
            
            <div class="practice-section">
                <div class="practice-label">🌅 Morning Practice (10-15 minutes):</div>
                <div class="practice-content">{day_data['morning_practice']}</div>
            </div>
            
            <div class="practice-section">
                <div class="practice-label">🌞 Daily Integration:</div>
                <div class="practice-content">{day_data['daily_integration']}</div>
            </div>
            
            <div class="practice-section">
                <div class="practice-label">🌙 Evening Reflection:</div>
                <div class="practice-content">{day_data['evening_reflection']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Long-term guidance
    st.markdown(f"""
    <div class="content-card" style="background: rgba(139, 69, 19, 0.05);">
        <h3 style="color: #5D4E37; margin-bottom: 1rem;">🌱 Continuing Your Journey</h3>
        <p style="color: #6B5B47; line-height: 1.7;">{technique_data['long_term_guidance']}</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main app function"""
    # Initialize session state
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'intro'
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 1
    
    # Render header
    render_header()
    
    # Handle different steps
    if st.session_state.current_step == 'intro':
        render_intro()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🧘‍♀️ Begin Your Journey", type="primary"):
                st.session_state.current_step = 'assessment'
                st.rerun()
    
    elif st.session_state.current_step == 'assessment':
        current_q = st.session_state.current_question
        
        # Render progress
        render_progress_bar(current_q, len(QUESTIONS))
        
        # Render current question
        question_data = QUESTIONS[current_q - 1]
        question_key = f"question_{current_q}"
        
        keywords = render_question(question_data, question_key)
        
        # Navigation
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_q > 1:
                if st.button("⬅️ Previous", key="prev_btn"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if keywords:  # Only show next if option is selected
                if current_q < len(QUESTIONS):
                    if st.button("Next ➡️", key="next_btn", type="primary"):
                        st.session_state.answers[str(current_q)] = keywords
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("✨ Generate Practice", key="generate_btn", type="primary"):
                        st.session_state.answers[str(current_q)] = keywords
                        st.session_state.current_step = 'generating'
                        st.rerun()
    
    elif st.session_state.current_step == 'generating':
        st.markdown("""
        <div class="content-card" style="text-align: center;">
            <h2 style="color: #5D4E37;">🧘‍♂️ Connecting with AI Wisdom Teacher...</h2>
            <p style="color: #7B6143; font-style: italic; margin: 2rem 0;">
                Crafting your personalized practice from ancient Buddhist teachings
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show spinner
        with st.spinner("Generating your personalized equanimity practice..."):
            technique_data = call_api(st.session_state.answers)
        
        if technique_data:
            st.session_state.technique_data = technique_data
            st.session_state.current_step = 'results'
            st.rerun()