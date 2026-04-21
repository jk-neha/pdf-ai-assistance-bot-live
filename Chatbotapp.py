import streamlit as st
import PyPDF2
from groq import Groq

import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# =========================
# PDF TEXT EXTRACTION
# =========================
def extract_pdf_text(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"

    return text


# =========================
# ASK AI (GROQ)
# =========================
# def ask_ai(context, question):

#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant. Answer only from context."},
#             {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
#         ]
#     )

#     return response.choices[0].message.content

def ask_ai(context, question):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer only from context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    )

    return response.choices[0].message.content
# =========================
# STREAMLIT UI
# =========================
st.title("📄 PDF Chatbot (PRO VERSION)")

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_pdf:

    pdf_text = extract_pdf_text(uploaded_pdf)
    st.success("PDF loaded successfully ✅")

    question = st.text_input("Ask a question")

    if st.button("Get Answer"):

        if question.strip():

            context = pdf_text[:4000]

            with st.spinner("Thinking... 🤖"):
                answer = ask_ai(context, question)

            st.markdown("### 🧠 Answer")
            st.write(answer)

        else:
            st.warning("Enter a question")