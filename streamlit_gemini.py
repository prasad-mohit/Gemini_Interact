import streamlit as st  
import asyncio  
import aiohttp  
import json  
from datetime import datetime, timedelta  
  
# Assuming google.generativeai as a placeholder module as it doesn't exist.  
# You would replace this with the actual module you're using to interact with Gemini API.  
import google.generativeai as genai  
  
# Initialize conversation history if it doesn't exist  
if 'conversation' not in st.session_state:  
    st.session_state.conversation = []  
  
# Configure Gemini with API key  
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY"))  
  
# Model selection  
model_options = ["models/gemini-1.5-flash", "models/gemini-1.5-pro"]  
selected_model = st.selectbox("Select a model", model_options)  
model = genai.GenerativeModel(model_name=selected_model)  
  
# Get user input  
user_input = st.text_input("Ask me anything", key="user_input")  
  
async def get_response(user_input):  
    # Add user message to conversation  
    st.session_state.conversation.append({"role": "user", "content": user_input})  
  
    # Generate response from the model  
    async with aiohttp.ClientSession() as session:  
        response = await model.generate(session, prompts=st.session_state.conversation)  
        return response  
  
def show_conversation():  
    # Display conversation history  
    for chat in st.session_state.conversation:  
        role = chat['role']  
        content = chat['content']  
        if role == "user":  
            st.text_area("", content, key=f"user_{len(st.session_state.conversation)}", height=50)  
        else:  
            st.text_area("", content, key=f"model_{len(st.session_state.conversation)}", height=50)  
  
if user_input:  
    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)  
    response = loop.run_until_complete(get_response(user_input))  
      
    # Add model response to conversation  
    st.session_state.conversation.append({"role": "model", "content": response})  
      
    # Reset user input  
    st.session_state.user_input = ""  
  
# Show conversation history  
show_conversation()  
