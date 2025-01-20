import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pyttsx3
import threading
import time

# Configure the page
st.set_page_config(
    page_title="J.A.R.V.I.S",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Iron Man themed UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500&display=swap');
    
    /* Main background and text colors */
    .stApp {
        background-color: #1a1a1a;
        color: #00fff2;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Header styling */
    .title-container {
        background: linear-gradient(90deg, #000000, #1a1a1a);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00fff2;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        position: relative;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .user-message {
        background-color: rgba(0, 89, 179, 0.2);
        border: 1px solid #007acc;
    }
    
    .bot-message {
        background-color: rgba(0, 255, 242, 0.1);
        border: 1px solid #00fff2;
    }
    
    /* Input box styling */
    .stTextInput input {
        background-color: #2d2d2d !important;
        color: #00fff2 !important;
        border: 2px solid #00fff2 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    .stTextInput input:focus {
        box-shadow: 0 0 10px #00fff2 !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: transparent !important;
        color: #00fff2 !important;
        border: 2px solid #00fff2 !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #00fff2 !important;
        color: #1a1a1a !important;
        box-shadow: 0 0 20px #00fff2 !important;
    }
    
    /* Animation keyframes */
    @keyframes glow {
        from {
            box-shadow: 0 0 5px #00fff2, 0 0 10px #00fff2, 0 0 15px #00fff2;
        }
        to {
            box-shadow: 0 0 10px #00fff2, 0 0 20px #00fff2, 0 0 30px #00fff2;
        }
    }
    
    /* System status styling */
    .system-status {
        background-color: rgba(0, 255, 242, 0.1);
        border: 1px solid #00fff2;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Time display */
    .time-display {
        color: #00fff2;
        font-size: 1.2em;
        text-align: right;
        margin-bottom: 10px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00fff2;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize text-to-speech engine
def speak_text(text):
    engine = pyttsx3.init()
    # Customize voice settings
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    
    # Get available voices and set a male voice
    voices = engine.getProperty('voices')
    for voice in voices:
        # Usually, voice[1] is a male voice in most systems
        if "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    engine.say(text)
    engine.runAndWait()

# Function to play welcome message in a separate thread
def play_welcome_message():
    welcome_text = "Alpha-One, this is Jarvis, code X01, its an advanced system born from the mind of , Mr.Ritesh Sakhare , Gen AI developer. We are Ready to crush the limits of innovation."
    threading.Thread(target=speak_text, args=(welcome_text,), daemon=True).start()

# Add this at the beginning of your main() function, right after the page config
def initialize_session():
    if 'welcomed' not in st.session_state:
        st.session_state.welcomed = False
        
    if not st.session_state.welcomed:
        play_welcome_message()
        st.session_state.welcomed = True

def initialize_gemini():
    GOOGLE_API_KEY = "AIzaSyBJFSzwJPdM9q03kDMekBkXwLZ35RfTTiM"
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

def get_response(model, message, chat_history):
    # Add some Jarvis-like personality to the response
    context = """You are J.A.R.V.I.S. (Just A Rather Very Intelligent System), 
    Tony Stark's AI assistant. Respond in a formal, sophisticated manner while 
    maintaining efficiency and precision. Use technical terminology when appropriate."""
    
    full_message = f"{context}\n\nUser message: {message}"
    response = model.generate_content(full_message)
    return response.text

def display_system_status():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="system-status">
                🔋 Power Systems: Online
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="system-status">
                🛡️ Defense Systems: Active
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="system-status">
                📡 Network Status: Connected
            </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize welcome message
    initialize_session()
    
    # Display title with custom styling
    st.markdown("""
        <div class="title-container">
            <h1>⚡J.A.R.V.I.S. CBOT⚡</h1>
            <p>Created by Ritesh Sakhare</p>
        </div>
    """, unsafe_allow_html=True)

    # Display current time
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="time-display">
            System Time: {current_time}
        </div>
    """, unsafe_allow_html=True)

    # Display system status
    display_system_status()

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "model" not in st.session_state:
        st.session_state.model = initialize_gemini()

    # Chat interface
    user_input = st.text_input("Input Command:", key="user_input", 
                              placeholder="How may I assist you, sir?")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send Command"):
            if user_input:
                st.session_state.chat_history.append(("user", user_input))
                with st.spinner("Processing..."):
                    bot_response = get_response(st.session_state.model, 
                                             user_input, 
                                             st.session_state.chat_history)
                    st.session_state.chat_history.append(("bot", bot_response))
    
    with col2:
        if st.button("Clear Systems"):
            st.session_state.chat_history = []

    # Display chat history
    for role, message in reversed(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div><strong>Command Input:</strong></div>
                    <div>{message}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <div><strong>J.A.R.V.I.S.:</strong></div>
                    <div>{message}</div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()