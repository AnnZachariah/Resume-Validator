import base64
import io
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_rep(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process uploaded PDF
def input_pdf(file_bytes):
    try:
        poppler_path = r"C:\Users\annza\Documents\tp wks\ATS\poppler-24.08.0\Library\bin"
        # Convert PDF bytes to images
        images = pdf2image.convert_from_bytes(file_bytes, poppler_path=poppler_path)
        first_page = images[0]

        # Convert image to bytes
        image_byte_array = io.BytesIO()
        first_page.save(image_byte_array, format='JPEG')
        image_byte_array = image_byte_array.getvalue()

        # Prepare PDF content
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_array).decode()
            }
        ]
        return pdf_parts
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# Streamlit App
st.set_page_config(page_title="ATS Resume Validator", layout="centered")
st.title("ATS Resume Validator")
st.write("Upload your resume in PDF format and provide the job description.")

# Input Fields
input_text = st.text_area("Enter the job description:", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

# Read file bytes once
file_bytes = None
if uploaded_file is not None:
    file_bytes = uploaded_file.read()  # Read file bytes once
    st.success("PDF Uploaded Successfully!")

# Buttons
submit1 = st.button("Tell me about the Resume")
submit4 = st.button("Percentage Match")

# Prompts
input_prompt1 = """
 You are an experienced Technical Human Resource Manager in the field of Data Science, Full stack web development, Big data engineering, Devops, Azure, Data Analyst, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Button Handlers
if submit1:
    if file_bytes:
        pdf_content = input_pdf(file_bytes)
        if pdf_content:
            response = get_gemini_rep(input_prompt1, pdf_content, input_text)
            st.subheader("Resume Evaluation:")
            st.write(response)
    else:
        st.warning("Please upload a resume.")

if submit4:
    if file_bytes:
        pdf_content = input_pdf(file_bytes)
        if pdf_content:
            response = get_gemini_rep(input_prompt3, pdf_content, input_text)
            st.subheader("Percentage Match:")
            st.write(response)
    else:
        st.warning("Please upload a resume.")
