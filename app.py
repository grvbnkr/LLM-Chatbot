import streamlit as st
import PyPDF2
import google.generativeai as genai

genai.configure(api_key="AIzaSyDVv4B18KVv95-HPG4yUgjOlzQULzRMIp4")

st.title("📄 LLM-powered PDF Q&A Chatbot by Gaurav")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    st.text_area("📄 Extracted Text", text[:1000] + "...", height=200)

    question = st.text_input("❓ Ask a question about the PDF")

    if question and text:
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                 question,
                 generation_config={
        "max_output_tokens": 300
        }
        )
            # Inspect the response
        print(response)  # This will help you understand its structure
        # or
        print(dir(response))  # List all available attributes and methods

        # Try accessing the response content using the correct attribute
        if hasattr(response, 'txt'):
            answer = response.text
        else:
            # If there's no txt attribute, check for an alternative attribute like 'content'
            answer = response.candidates[0].content.parts[0].text  # or another attribute depending on the structure
        st.success("💬 Answer:")
        st.write(answer)
