#to get your own api key visit -https://platform.openai.com/api-keys
#to install dependencies - pip install streamlit openai PyPDF2
#to run this script - python -m streamlit run pdf_openai_gui.py
import streamlit as st
import PyPDF2
import openai
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key="apni api key khud bhare")  # Replace with your key

#  PDF Text Extractor 
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

#  Summarizer 
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or any other model
        messages=[
            {"role": "system", "content": "Summarize this text."},
            {"role": "user", "content": text}
        ],
        temperature=0.5,
        max_tokens=1024
    )
    return response.choices[0].message.content

#  Question based on Context 
def ask_question(context, question):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer the question based on the given context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ],
        temperature=0.7,
        max_tokens=512
    )
    return response.choices[0].message.content

#  GUI
st.set_page_config(page_title="PDF AI Assistant", layout="wide")
st.title("📄 PDF AI Assistant")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("PDF uploaded successfully.")
    with st.spinner("Extracting and summarizing PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        if text:
            summary = summarize_text(text)
            st.subheader("📌 PDF Summary")
            st.write(summary)

            st.subheader("❓ Ask Questions About the PDF")
            user_question = st.text_input("Enter your question")
            if user_question:
                with st.spinner("Getting answer..."):
                    answer = ask_question(text, user_question)
                    st.write("🧠 Answer:", answer)
        else:
            st.warning("Could not extract any text from the PDF.")

