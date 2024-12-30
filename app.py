import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
import uuid

st.set_page_config(layout="wide")

def text_summary(text, maxlength=None):
    # Create summary instance
    summary = Summary()
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    try:
        # Open the PDF file using PyPDF2
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()  # Concatenate text from all pages
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if input_text and input_text.strip():  # Check for empty text
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file is not None:
        unique_file_name = f"doc_{uuid.uuid4().hex}.pdf"  # Generate unique file name
        with open(unique_file_name, "wb") as f:
            f.write(input_file.getbuffer())
        if st.button("Summarize Document"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("File uploaded successfully")
                extracted_text = extract_text_from_pdf(unique_file_name)
                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text)
            with col2:
                st.markdown("**Summary Result**")
                doc_summary = text_summary(extracted_text)
                st.success(doc_summary)
