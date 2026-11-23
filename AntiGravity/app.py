import streamlit as st
import database
import extractor
import ai_service

# Initialize database
database.init_db()

# Page configuration
st.set_page_config(
    page_title="AI Smart Notes | ZCOER",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
    }
    .card-box {
        border-radius: 8px;
        padding: 1rem;
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
col_header, col_badge = st.columns([3, 1])
with col_header:
    st.markdown('<div class="main-title">AI-Based Smart Notes Application</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Zeal College of Engineering & Research, Pune • Dept. of Electronics & Computer Engineering</div>', unsafe_allow_html=True)
with col_badge:
    st.markdown('<div style="text-align: right; padding-top: 15px;"><span class="badge">Review 1: 50% Milestone</span></div>', unsafe_allow_html=True)

st.divider()

# Sidebar: Configuration & History
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input(
        "Google Gemini API Key (Optional)",
        type="password",
        placeholder="Paste AI Studio Key or leave blank for demo",
        help="Free key from aistudio.google.com. If blank, built-in demo mode runs."
    )
    
    st.subheader("📚 Academic Metadata")
    semester = st.selectbox(
        "Select Semester",
        ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5", "Semester 6", "Semester 7", "Semester 8"],
        index=4
    )
    subject = st.text_input("Course / Subject Name", value="Machine Learning & AI")
    
    st.divider()
    st.subheader("👥 Project Team")
    st.caption("**Snehalish Zode** (EC3347)")
    st.caption("**Swayam Sonawane** (EC3331)")
    st.caption("**Krishna Wajage** (EC3341)")
    st.caption("Coordinator: Prof. Sana A. Metkari")

# Main Interface Tabs
tab_create, tab_history = st.tabs(["📤 Upload & Process Document", "📂 Saved Knowledge Repository"])

with tab_create:
    st.subheader("1. Ingest Academic PDF")
    uploaded_file = st.file_uploader("Upload lecture slide, notes, or research paper PDF", type=["pdf"])

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            process_btn = st.button("🚀 Process with AI", type="primary", use_container_width=True)
        with col_info:
            st.info(f"File loaded: **{uploaded_file.name}** ({len(file_bytes) / 1024:.1f} KB)")
        
        if process_btn:
            with st.spinner("Extracting text with PyMuPDF & generating structured learning notes..."):
                # Step 1: Extraction
                extracted_text = extractor.extract_text_from_pdf(file_bytes)
                
                if not extracted_text:
                    st.error("No readable text found in PDF. Make sure it is not a scanned image without OCR.")
                else:
                    # Step 2: AI Synthesis
                    result = ai_service.analyze_document_content(extracted_text, api_key=api_key)
                    
                    topic_name = result.get("topic_name", "Academic Note")
                    summary = result.get("summary", "")
                    definitions = result.get("key_definitions", [])
                    flashcards = result.get("flashcards", [])
                    
                    # Step 3: Save to SQLite
                    note_id = database.save_note(
                        subject=subject,
                        semester=semester,
                        topic_name=topic_name,
                        raw_text=extracted_text,
                        summary=summary,
                        key_definitions=definitions,
                        flashcards=flashcards
                    )
                    
                    st.success(f"✅ Successfully processed and indexed note #{note_id}: **{topic_name}**")
                    
                    # Display Results
                    st.divider()
                    st.markdown(f"### 📌 Topic: {topic_name}")
                    st.caption(f"**Semester:** {semester} | **Subject:** {subject} | **Source:** {uploaded_file.name}")
                    
                    # 50% Milestone Preview of Upcoming Core Feature
                    st.info("""
                    **🔔 Preview of 100% Core Feature (Semantic Memory Engine):**  
                    In the next phase, `all-MiniLM-L6-v2` embeddings will compare this note with earlier semesters (e.g., Sem 2 Linear Algebra) 
                    and trigger automated prerequisite recall notifications!
                    """)
                    
                    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
                        "📝 Structured Summary", 
                        "🗂️ Interactive Flashcards", 
                        "📖 Key Definitions",
                        "📄 Extracted Text"
                    ])
                    
                    with sub_tab1:
                        st.markdown(summary)
                        
                    with sub_tab2:
                        st.markdown("Test your recall with auto-generated concept flashcards:")
                        for idx, card in enumerate(flashcards, start=1):
                            with st.expander(f"Question {idx}: {card['question']}"):
                                st.success(f"**Answer:** {card['answer']}")
                                
                    with sub_tab3:
                        for definition in definitions:
                            st.markdown(f"- {definition}")
                            
                    with sub_tab4:
                        st.text_area("Preprocessed Text Sample (First 2000 chars)", extracted_text[:2000], height=250)

with tab_history:
    st.subheader("Personal Learning History")
    all_notes = database.get_all_notes()
    
    if not all_notes:
        st.info("No notes saved in your learning repository yet. Upload a document to build history.")
    else:
        st.write(f"Total Saved Notes: **{len(all_notes)}**")
        for item in all_notes:
            with st.expander(f"[{item['semester']}] {item['subject']} — {item['topic_name']} ({item['created_at']})"):
                st.markdown(f"**Summary:**\n{item['summary']}")
                st.caption(f"Note Record ID: #{item['id']}")
