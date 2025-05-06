import streamlit as st  
import google.generativeai as genai  
import cv2  
import numpy as np  
from PIL import Image  
import os  
import torch  
from ultralytics import YOLO  
  
# Configure Gemini API key  
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  
  
# Initialize the Gemini model  
model = genai.GenerativeModel('gemini-1.5-flash')  
  
# Load YOLO model (make sure the YOLO weights are available locally or via URL)  
yolo_model = YOLO("yolov8n.pt")  # Replace with a specific model if needed  
  
# Streamlit app setup  
st.title("Sakman Horticulture Image Analysis")  
st.write("Upload a clear photo of your Horticulture product to analyze its quality and check for diseases.")  
  
# Crop type selection  
crop_type = st.selectbox("Select crop type", ["Tea Leaf", "Apple", "Other"])  
if crop_type == "Other":  
    crop_type = st.text_input("Enter crop type", "Specify crop")  
  
# Image uploader  
image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])  
  
# Prompt input  
default_prompt = f"Analyze this {crop_type} for quality and any diseases."  
prompt = st.text_input("Enter your question", value=default_prompt)  
  
# YOLO bounding box visualization function  
def visualize_yolo(image):  
    # Convert PIL image to NumPy array  
    image_array = np.array(image)  
      
    # Perform YOLO inference  
    results = yolo_model(image_array)  
      
    # Get bounding box details  
    annotated_image = results[0].plot()  # Annotated image with bounding boxes  
      
    # Convert back to PIL for Streamlit display  
    annotated_image = Image.fromarray(annotated_image)  
    return annotated_image  
  
# Graphical representation function  
def graphical_output(response_text):  
    st.write("### Graphical Representation:")  
      
    # Quality meter  
    st.write("**Quality Meter:**")  
    if "high quality" in response_text.lower():  
        st.progress(100)  
    elif "medium quality" in response_text.lower():  
        st.progress(50)  
    else:  
        st.progress(10)  
      
    # Pest problem  
    st.write("**Pest Problem:**")  
    if "pest detected" in response_text.lower():  
        st.image("red_pest_icon.png", width=50)  # Replace with actual pest icon file path  
    else:  
        st.image("green_tick_icon.png", width=50)  # Replace with actual tick icon file path  
      
    # Inedible status  
    st.write("**Inedible Status:**")  
    if "inedible" in response_text.lower():  
        st.image("red_x_icon.png", width=50)  # Replace with actual X icon file path  
    else:  
        st.image("green_tick_icon.png", width=50)  # Replace with actual tick icon file path  
  
# Process and display response  
if st.button("Get Response"):  
	if image_file is not None:  
        	try:  
        	    # Open uploaded image  
            	image = Image.open(image_file)  
              
            	# Display original image  
            	st.image(image, caption="Uploaded Image", use_column_width=True)  
              
            	# Visualize YOLO bounding boxes  
            	annotated_image = visualize_yolo(image)  
            	st.image(annotated_image, caption="YOLO Detection", use_column_width=True)  
              
            	# Generate response using Gemini  
            	response = model.generate_content([image, prompt])  
              
            	# Display analysis result  
            	st.write("### Analysis Result:")  
            	st.write(response.text)  
              
            	# Graphical representation of the result  
            	graphical_output(response.text)  
        	except Exception as e:  
            		st.error(f"An error occurred: {str(e)}")  
	else:
		st.warning("Please upload an image.")  
