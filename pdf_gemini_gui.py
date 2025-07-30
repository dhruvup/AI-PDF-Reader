#for api keys visit- https://aistudio.google.com/
#install dependenncies- pip install streamlit google-generativeai pymupdf
#to run this - python -m streamlit run pdf_gemini_gui.py
import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Gemini API
genai.configure(api_key="apni api key khud bhare")
model = genai.GenerativeModel("gemini-1.5-pro")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

# Function to summarize
def summarize_text(text):
    prompt = f"Summarize the following document:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Function to answer question
def answer_question(text, question):
    prompt = f"""Based on the following document:\n\n{text}\n\nAnswer this question:\n{question}"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit for UI
st.set_page_config(page_title="📄 Gemini PDF Summarizer & QnA", layout="centered")

st.title("📄 Gemini PDF Summarizer + ")
pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

if pdf_file:
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(pdf_file)
        st.success("PDF text extracted successfully!")

    if st.button("Summarize PDF"):
        with st.spinner("Summarizing with Gemini..."):
            summary = summarize_text(text)
            st.subheader("📝 Summary")
            st.write(summary)

    question = st.text_input("Ask a question about the PDF")
    if question:
        with st.spinner("Answering..."):
            answer = answer_question(text, question)
            st.subheader("💬 Answer")
            st.write(answer)
