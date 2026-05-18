import streamlit as st
from groq import Groq
import PyPDF2
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Neha AI PDF Assistant",
    page_icon="💬|pdf",
    layout="wide"
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Base ── */
.stApp {
    background-color: #0D0D0D;
    color: #E8E6E0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #1E1E1E;
}

section[data-testid="stSidebar"] * {
    color: #C8C6C0 !important;
}

section[data-testid="stSidebar"] h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.01em;
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #444240 !important;
    margin-bottom: 14px !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 13px !important;
    line-height: 2.2 !important;
    color: #7A7876 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #1E1E1E !important;
    margin: 20px 0 !important;
}

section[data-testid="stSidebar"] .stCaption p {
    color: #333130 !important;
    font-size: 11px !important;
}

/* ── Main title ── */
.main-title {
    font-family: 'Syne', sans-serif;
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 36px 0 8px 0;
    letter-spacing: -0.04em;
    line-height: 1.05;
}

.title-accent {
    color: #7C6AF5;
}

.sub-title {
    text-align: center;
    color: #444240;
    font-size: 16px;
    font-weight: 300;
    margin-bottom: 32px;
}

/* ── Badge strip ── */
.badge-strip {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 40px;
}

.badge {
    background: #161616;
    border: 1px solid #2A2A2A;
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 12px;
    color: #7C6AF5;
    font-weight: 500;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: #1E1E1E;
    margin: 28px 0;
}

/* ── Upload Box ── */
[data-testid="stFileUploader"] {
    background: #111111 !important;
    border: 1.5px dashed #2A2A2A !important;
    border-radius: 16px !important;
    padding: 28px 22px !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p {
    color: #E8E6E0 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #444240 !important;
}

/* Upload "Browse files" button */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stBaseButton-secondary"] {
    background: #1E1E1E !important;
    color: #E8E6E0 !important;
    border: 1px solid #3A3A3A !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}

[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stBaseButton-secondary"]:hover {
    background: #7C6AF5 !important;
    border-color: #7C6AF5 !important;
    color: #FFFFFF !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: #0F1A14 !important;
    border: 1px solid #1E3A28 !important;
    border-radius: 12px !important;
    font-size: 14px !important;
}

[data-testid="stAlert"] p {
    color: #6EE89A !important;
}

/* ── Text Input ── */
.stTextInput > label {
    color: #5A5856 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
}

.stTextInput input {
    background-color: #111111 !important;
    color: #FFFFFF !important;
    border: 1.5px solid #2A2A2A !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    caret-color: #7C6AF5 !important;
}

.stTextInput input:focus {
    border-color: #7C6AF5 !important;
    box-shadow: 0 0 0 3px rgba(124, 106, 245, 0.15) !important;
}

.stTextInput input::placeholder {
    color: #2E2C2A !important;
}

/* ── Action Buttons ── */
.stButton > button {
    width: 100%;
    background: #161616 !important;
    color: #C8C6C0 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 10px !important;
    padding: 12px 8px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em;
    transition: all 0.18s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: #7C6AF5 !important;
    border-color: #7C6AF5 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Primary "Ask AI" — first column */
div[data-testid="column"]:first-child .stButton > button {
    background: #7C6AF5 !important;
    border-color: #7C6AF5 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

div[data-testid="column"]:first-child .stButton > button:hover {
    background: #6354D4 !important;
    border-color: #6354D4 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: #444240 !important;
    font-size: 14px !important;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: #111111 !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 14px !important;
    padding: 18px 20px !important;
    margin-bottom: 10px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #C8C6C0 !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}

[data-testid="stChatMessage"] strong {
    color: #FFFFFF !important;
}

[data-testid="stChatMessage"] code {
    background: #1A1A1A !important;
    color: #A8FFC4 !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
}

/* ── Markdown outside chat ── */
.stMarkdown p,
.stMarkdown li {
    color: #8A8880 !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
}

.stMarkdown h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.02em !important;
    border-bottom: 1px solid #1E1E1E !important;
    padding-bottom: 8px !important;
    margin-top: 12px !important;
}

.stMarkdown h3 {
    color: #C8C6C0 !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 70px;
    margin-bottom: 30px;
    color: #222220;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0D0D0D; }
::-webkit-scrollbar-thumb { background: #222220; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7C6AF5; }

</style>
""", unsafe_allow_html=True)

# ---------------- PDF EXTRACTION ----------------
def extract_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        if reader.is_encrypted:
            reader.decrypt("")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"PDF Error: {e}")
        return None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Neha AI")
    st.markdown("---")
    st.markdown("""
### Features

✦ PDF Question Answering  
✦ AI Summarization  
✦ Resume Analyzer  
✦ Interview Question Gen  
✦ Research Assistant  
""")
    st.markdown("---")
    st.caption("Built with Streamlit · Powered by Groq")

# ---------------- TITLE ----------------
st.markdown(
    '<h1 class="main-title">PDF <span class="title-accent">Intelligence</span></h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-title">Upload any document — ask questions, get summaries, and deep analysis instantly</p>',
    unsafe_allow_html=True
)

# Capability badges
st.markdown("""
<div class="badge-strip">
  <span class="badge">✦ Q&amp;A</span>
  <span class="badge">✦ Summarize</span>
  <span class="badge">✦ Resume Analysis</span>
  <span class="badge">✦ Interview Prep</span>
  <span class="badge">✦ Research Mode</span>
</div>
""", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
uploaded_pdf = st.file_uploader(
    "Upload your PDF to get started",
    type=["pdf"]
)

# ---------------- MAIN LOGIC ----------------
if uploaded_pdf:

    pdf_text = extract_pdf_text(uploaded_pdf)

    if pdf_text:

        st.success("✓  Document ready — choose an action below")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        question = st.text_input(
            "Ask a question about the document",
            placeholder="e.g. What are the key findings in this paper?"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            ask_btn = st.button("Ask AI")

        with col2:
            summary_btn = st.button("Summarize")

        with col3:
            resume_btn = st.button("Resume Analysis")

        with col4:
            interview_btn = st.button("Interview Qs")

        with col5:
            research_btn = st.button("Research Mode")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ---------------- QUESTION ANSWERING ----------------
        if ask_btn and question:
            with st.spinner("Thinking..."):
                prompt = f"""
                Answer only from the PDF content.

                PDF:
                {pdf_text}

                Question:
                {question}
                """
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = completion.choices[0].message.content

                with st.chat_message("user"):
                    st.markdown(question)

                with st.chat_message("assistant"):
                    st.markdown(answer)

        # ---------------- SUMMARY ----------------
        if summary_btn:
            with st.spinner("Generating summary..."):
                summary_prompt = f"""
                Summarize this PDF clearly and professionally:

                {pdf_text}
                """
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": summary_prompt}]
                )
                summary = completion.choices[0].message.content

                with st.chat_message("assistant"):
                    st.markdown("## PDF Summary")
                st.markdown(summary)

        # ---------------- RESUME ANALYZER ----------------
        if resume_btn:
            with st.spinner("Analyzing resume..."):
                resume_prompt = f"""
                Analyze this resume professionally.

                Give:
                1. ATS Score out of 100
                2. Technical Skills Found
                3. Missing Skills
                4. Resume Strengths
                5. Resume Weaknesses
                6. Suggestions to Improve
                7. Best Job Roles suited

                Resume:
                {pdf_text}
                """
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": resume_prompt}]
                )
                resume_analysis = completion.choices[0].message.content

                with st.chat_message("assistant"):
                    st.markdown("## Resume Analysis")
                    st.markdown(resume_analysis)

        # ---------------- INTERVIEW QUESTIONS ----------------
        if interview_btn:
            with st.spinner("Generating interview questions..."):
                interview_prompt = f"""
                Based on this resume/document,
                generate:

                1. HR Interview Questions
                2. Technical Interview Questions
                3. Project-Based Questions
                4. Coding Questions
                5. Behavioral Questions

                Resume:
                {pdf_text}
                """
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": interview_prompt}]
                )
                interview_questions = completion.choices[0].message.content

                with st.chat_message("assistant"):
                    st.markdown("## Interview Questions")
                    st.markdown(interview_questions)

        # ---------------- RESEARCH MODE ----------------
        if research_btn:
            with st.spinner("Running research analysis..."):
                research_prompt = f"""
                Explain this document like a research assistant.

                Include:
                1. Main Topic
                2. Key Insights
                3. Important Concepts
                4. Technical Explanation
                5. Simple Explanation for Beginners
                6. Real-world Applications
                7. Final Conclusion

                Document:
                {pdf_text}
                """
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": research_prompt}]
                )
                research_output = completion.choices[0].message.content

                with st.chat_message("assistant"):
                    st.markdown("## Research Analysis")
                    st.markdown(research_output)

# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">Made with ❤ by Neha Vardhini</div>',
    unsafe_allow_html=True
)