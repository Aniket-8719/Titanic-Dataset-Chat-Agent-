import base64
import fastapi
import pandas as pd
import langchain
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from fastapi import FastAPI
from langchain.llms import OpenAI
from pydantic import BaseModel
from io import BytesIO

# Load dataset
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Titanic Chatbot!"}

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_data(request: QueryRequest):
    query = request.query.lower()
    
    if "percentage of passengers were male" in query:
        male_percentage = (df['Sex'].value_counts(normalize=True)['male'] * 100)
        return {"response": f"{male_percentage:.2f}% of passengers were male."}
    
    elif "average ticket fare" in query:
        avg_fare = df['Fare'].mean()
        return {"response": f"The average ticket fare was ${avg_fare:.2f}."}
    
    elif "passengers embarked from each port" in query:
        embark_counts = df['Embarked'].value_counts().to_dict()
        return {"response": embark_counts}
    
    elif "histogram of passenger ages" in query:
        fig, ax = plt.subplots()
        sns.histplot(df['Age'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title("Histogram of Passenger Ages")
        ax.set_xlabel("Age")
        ax.set_ylabel("Count")

        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)  # Close the figure to free memory

        # Encode image in Base64
        base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
        
        return {"image": base64_image}
    
    else:
        return {"response": "I'm not sure how to answer that yet!"}

# Streamlit UI
st.title("🚢 Titanic Dataset Chatbot")
query = st.text_input("Ask a question about the Titanic dataset:")

if st.button("Submit"):
    response = query_data(QueryRequest(query=query))
    
    if "image" in response:
        # Decode Base64 image and display it
        st.image(BytesIO(base64.b64decode(response["image"])), caption="Histogram of Passenger Ages")
    else:
        st.write(response["response"])
