import streamlit as st
import requests
import base64
from io import BytesIO

API_URL = "https://titanic-dataset-chat-agent.onrender.com/query"  # Adjust if needed

st.title("🚢 Titanic Dataset Chatbot")

# User input field
query = st.text_input("Ask a question about the Titanic dataset:")

# Predefined question dropdown
predefined_questions = [
    "What percentage of passengers were male on the Titanic?",
    "Show me a histogram of passenger ages",
    "What was the average ticket fare?",
    "How many passengers embarked from each port?"
]

selected_question = st.selectbox("Or select a predefined question:", ["Select a question..."] + predefined_questions)

# If a question is selected from the dropdown, update the input field
if selected_question != "Select a question...":
    query = selected_question

if st.button("Submit"):
    if query:  # Ensure the query is not empty
        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            data = response.json()

            if "response" in data:
                st.write(data["response"])  # Display text response
            elif "image" in data:
                # Decode Base64 image and display it
                image_bytes = base64.b64decode(data["image"])
                st.image(BytesIO(image_bytes), caption="Histogram of Passenger Ages")
            else:
                st.write("Unexpected response format!")
        else:
            st.error("Error fetching response from API.")
    else:
        st.warning("Please enter or select a question before submitting.")
