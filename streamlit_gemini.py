import streamlit as st  
import asyncio  
import aiohttp  
import json  
  
# Assuming 'google.generativeai' and 'genai.GenerativeModel' are placeholders  
# You would replace these with the actual module and classes you're using  
import google.generativeai as genai  
  
# Initialize session state for conversation history if it doesn't exist  
if 'conversation' not in st.session_state:  
    st.session_state.conversation = []  
  
# Configure Gemini with API key  
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])  
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  
  
# Function to get response from Gemini model  
async def get_response(prompt):  
    try:  
        # Here you would implement the actual call to Gemini API  
        # For now, it's just a placeholder function that returns the prompt  
        # Replace with the actual API call  
        async with aiohttp.ClientSession() as session:  
            # Replace 'model.generate' with the actual Gemini API call  
            response = await model.generate(session, prompt=prompt)  
            return response  
    except Exception as e:  
        st.error(f"An error occurred: {e}")  
        return None  
  
# Function to display conversation  
def show_conversation():  
    for message in st.session_state.conversation:  
        if message['role'] == 'user':  
            st.text_area("", message['content'], key=f"user_{len(st.session_state.conversation)}", height=75, disabled=True)  
        else:  
            st.text_area("", message['content'], key=f"model_{len(st.session_state.conversation)}", height=75, disabled=True)  
  
# Streamlit layout  
st.title("Gemini Model Interaction")  
  
# User input  
user_input = st.text_input("Type your message here:", key="user_input")  
  
# Handling user input  
if user_input:  
    # Update conversation history with user input  
    st.session_state.conversation.append({"role": "user", "content": user_input})  
      
    # Run the async get_response function  
    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)  
    response = loop.run_until_complete(get_response(user_input))  
      
    # Update conversation history with model response  
    if response:  
        st.session_state.conversation.append({"role": "model", "content": response})  
  
    # Clear the input field after processing  
    st.session_state.user_input = ""  
  
# Display conversation history  
show_conversation()  
