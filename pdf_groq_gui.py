#install dependencies - pip install streamlit PyPDF2 requests
#To run the script- python -m streamlit run pdf_groq_chatbot.py
#for you api keys visit  - https://console.groq.com/keys
import streamlit as st
import PyPDF2
import requests

# SET YOUR GROQ API KEY 
GROQ_API_KEY = "apni api key khud bhare"  # Replace this with your Groq API key
MODEL = "llama3-70b-8192"  

# Function to call Groq Chat Completion
def groq_chat_completion(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "PDF reader AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

#  Streamlit UI 
st.set_page_config(page_title="PDF Reader AI", layout="wide")
st.title("📄 PDF AI Assistant (Groq + LLaMA 3)")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded.")
    with st.spinner("📖 Reading PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    if pdf_text.strip():
        with st.spinner("🧠 Summarizing with LLaMA 3..."):
            summary = groq_chat_completion(f"Summarize this content:\n\n{pdf_text}")
        st.subheader("📌 Summary")
        st.write(summary)

        st.subheader("❓ Ask Questions")
        user_question = st.text_input("What would you like to ask about the PDF?")
        if user_question:
            with st.spinner("🤔 Thinking..."):
                answer = groq_chat_completion(f"""Answer the following question based on this content:

Content:
{pdf_text}

Question:
{user_question}
""")
                st.write("🧠 Answer:", answer)
    else:
        st.warning("❗ No text could be extracted from the PDF.")
