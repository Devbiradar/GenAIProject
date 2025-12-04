import streamlit as st
import os
import sys
import tempfile
import json

# Add project root and src to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.resume_parser import extract_text_from_pdf, parse_resume
from src.rag_pipeline import RAGPipeline
from src.roadmap_engine import RoadmapEngine
from src.utils import create_pdf

# Page Config
st.set_page_config(
    page_title="CareerPathGPT",
    layout="wide"
)

# Custom CSS for Attractive Chat & Layout
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main Header */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        background: -webkit-linear-gradient(#1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    /* Glassmorphism Card Styling */
    .profile-card, .chat-container {
        background-color: rgba(255, 255, 255, 0.75); /* More transparent */
        backdrop-filter: blur(12px); /* Blur effect */
        -webkit-backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 25px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .profile-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.2);
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 3.5rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Engines
@st.cache_resource
def load_engines():
    rag = RAGPipeline()
    roadmap_engine = RoadmapEngine()
    return rag, roadmap_engine

rag, roadmap_engine = load_engines()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "generated_roadmap" not in st.session_state:
    st.session_state.generated_roadmap = None

# Sidebar
with st.sidebar:
    st.image("app/logo.png", width=280)
    st.title("CareerPathGPT")
    st.markdown("Your AI Career Companion")
    st.markdown("---")
    
    st.subheader("📂 Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Analyzing Resume..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                text = extract_text_from_pdf(tmp_path)
                data = parse_resume(text)
                st.session_state.resume_data = data
                st.success("Analysis Complete!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                os.remove(tmp_path)
    
    st.markdown("---")
    
    def clear_chat():
        st.session_state.messages = []
        
    st.button("🗑️ Clear Chat", on_click=clear_chat)

# Main Content
st.markdown('<div class="main-header">🚀 Career Guidance Dashboard</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# Left Column: Profile & Roadmap
with col1:
    st.subheader("📄 Your Profile")
    if st.session_state.resume_data:
        data = st.session_state.resume_data
        st.markdown(f"**Name:** {data.get('name', 'N/A')}")
        st.markdown(f"**Email:** {data.get('email', 'N/A')}")
        st.markdown(f"**Phone:** {data.get('phone', 'N/A')}")
        
        st.markdown("---")
        st.markdown("**🛠️ Skills:**")
        if data.get('skills'):
            st.info(", ".join(data['skills']))
        else:
            st.warning("No skills detected.")
            
        # Experience & Education in Expanders to save space
        with st.expander("💼 Experience"):
            for exp in data.get('experience', []):
                st.markdown(f"**{exp.get('role', 'Role')}** at {exp.get('company', 'Company')}")
                st.caption(exp.get('duration', ''))
        
        with st.expander("🎓 Education"):
            for edu in data.get('education', []):
                st.markdown(f"**{edu.get('degree', 'Degree')}** - {edu.get('institution', 'Uni')}")
                st.caption(edu.get('year', ''))
                
        st.markdown("---")
        st.subheader("🗺️ Generate Roadmap")
        target_role = st.text_input("Enter Target Role (e.g., Data Scientist)")
        
        if st.button("Generate Roadmap 🚀"):
            if not target_role:
                st.warning("Please enter a target role.")
            elif not data.get('skills'):
                st.warning("No skills found in resume.")
            else:
                with st.spinner("Crafting your roadmap..."):
                    roadmap = roadmap_engine.generate_roadmap(data['skills'], target_role)
                    st.session_state.generated_roadmap = roadmap
        
        if st.session_state.generated_roadmap:
            st.success("Roadmap Generated!")
            with st.expander("📍 View Roadmap", expanded=True):
                st.markdown(st.session_state.generated_roadmap)
            
            st.download_button(
                label="📥 Export Roadmap",
                data=st.session_state.generated_roadmap,
                file_name="career_roadmap.md",
                mime="text/markdown"
            )
            
            # Safe PDF Export
            try:
                pdf_bytes = create_pdf(st.session_state.generated_roadmap)
                st.download_button(
                    label="📄 Export to PDF",
                    data=pdf_bytes,
                    file_name="career_roadmap.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF Generation failed: {e}")
    else:
        st.info("👈 Please upload your resume in the sidebar to start.")

# Right Column: Chat
with col2:
    st.subheader("💬 Career Advisor")
    
    # Chat Interface
    # We use a container to mimic a chat window
    with st.container():
        for message in st.session_state.messages:
            avatar = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask for career advice..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                context_docs = rag.retrieve_relevant_careers(prompt)
                context_text = str(context_docs)
                response = rag.generate_response(context_text, prompt)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


