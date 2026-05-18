import streamlit as st
from groq import Groq
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Neha AI PDF Assistant",
    page_icon="📄",
    layout="wide"
)

import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Base ── */
.stApp {
    background-color: #F5F3EE;
    color: #1a1a1a;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #1C1C1E;
    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: #E8E6E0 !important;
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F5F3EE !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 15px !important;
    letter-spacing: 0.03em;
    margin-bottom: 12px !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #333335 !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 14px !important;
    line-height: 2 !important;
    color: #A8A6A0 !important;
}

/* Sidebar brand */
section[data-testid="stSidebar"] h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 22px !important;
    color: #F5F3EE !important;
    letter-spacing: -0.02em;
}

/* ── Hero Title ── */
.main-title {
    font-family: 'DM Serif Display', serif;
    text-align: center;
    font-size: 56px;
    font-weight: 400;
    color: #1C1C1E;
    margin: 30px 0 6px 0;
    letter-spacing: -0.03em;
    line-height: 1.1;
}

.title-accent {
    color: #C27D4A;
}

.sub-title {
    text-align: center;
    color: #7A7872;
    font-size: 17px;
    font-weight: 300;
    margin-bottom: 40px;
    letter-spacing: 0.01em;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #D4CFC6, transparent);
    margin: 28px 0;
}

/* ── Upload Box ── */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1.5px dashed #C8C4BC;
    border-radius: 16px;
    padding: 30px 24px;
    transition: border-color 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #C27D4A;
}

[data-testid="stFileUploader"] label {
    color: #1C1C1E !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploader"] small {
    color: #9A9690 !important;
}

/* ── Success / Info Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-size: 14px !important;
}

/* ── Text Input ── */
.stTextInput input {
    background-color: #FFFFFF !important;
    color: #1C1C1E !important;
    border: 1.5px solid #D4CFC6 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stTextInput input:focus {
    border-color: #C27D4A !important;
    box-shadow: 0 0 0 3px rgba(194, 125, 74, 0.12) !important;
}

.stTextInput input::placeholder {
    color: #B0ADA8 !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: #1C1C1E;
    color: #F5F3EE;
    border: none;
    border-radius: 12px;
    padding: 13px 10px;
    font-size: 13px;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.01em;
    transition: background 0.2s ease, transform 0.15s ease;
    cursor: pointer;
}

.stButton > button:hover {
    background: #C27D4A;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0px);
}

/* Primary ask button — first column */
div[data-testid="column"]:first-child .stButton > button {
    background: #C27D4A;
    font-size: 14px;
}

div[data-testid="column"]:first-child .stButton > button:hover {
    background: #A6682F;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: #7A7872 !important;
    font-size: 14px !important;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E8E4DC !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

[data-testid="stChatMessage"] p {
    font-size: 15px !important;
    line-height: 1.75 !important;
    color: #1C1C1E !important;
}

/* ── Headings in responses ── */
.stMarkdown h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    font-weight: 400;
    color: #1C1C1E;
    margin-top: 10px;
    letter-spacing: -0.02em;
}

/* ── Caption / Footer ── */
.footer {
    text-align: center;
    margin-top: 70px;
    margin-bottom: 30px;
    color: #B0ADA8;
    font-size: 13px;
    letter-spacing: 0.02em;
}

/* ── Sidebar caption ── */
section[data-testid="stSidebar"] .stCaption p {
    color: #5A5856 !important;
    font-size: 12px !important;
}

/* ── Badge strip ── */
.badge-strip {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 36px;
}

.badge {
    background: #FFFFFF;
    border: 1px solid #DDD9D2;
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 13px;
    color: #5A5856;
    font-weight: 400;
}

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