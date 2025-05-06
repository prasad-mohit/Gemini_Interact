import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro-vision')

# Streamlit app setup
st.title("Crop Leaf Analysis")
st.write("Upload a clear photo of your crop leaf to analyze its quality and check for diseases.")

# Crop type selection
crop_type = st.selectbox("Select crop type", ["Tea Leaf", "Apple", "Other"])
if crop_type == "Other":
    crop_type = st.text_input("Enter crop type", "Specify crop")

# Image uploader
image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

# Prompt input
default_prompt = f"Analyze this {crop_type} for quality and any diseases."
prompt = st.text_input("Enter your question", value=default_prompt)

# Process and display response
if st.button("Get Response"):
    if image_file is not None:
        try:
            image = Image.open(image_file)
            response = model.generate_content([image, prompt])
            st.write("**Analysis Result:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload an image.")
