import pandas as pd
import streamlit as st
from langchain_cohere import ChatCohere
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

@st.cache_data
def get_schema_details():
    df = pd.read_csv("mysql_schema_description.csv")
    schema = ""
    for _, row in df.iterrows():
        schema += f"Table Name: {row['Table_Name']}\nTable Description: {row['Description']}\n\n"
    return schema

# Prompt for follow-up suggestions
suggestion_prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant for SQL databases.
    Here is the recent conversation history:
    {history}

    Given the following database schema and the latest user question, suggest 2-3 relevant follow-up queries the user might want to ask next.
    Return your suggestions as a JSON array of strings, with no extra text, no code block, and no prefix. Only output the array.

    Database schema:
    {schema}

    Latest user question:
    {question}

    Suggested follow-up queries (JSON array):
    """
)

llm = ChatGroq(model='llama-3.3-70b-versatile', temperature=0.2)
json_parser = JsonOutputParser()

def clean_json_output(text):
    # Remove code block markers and leading 'json' if present
    import re
    text = re.sub(r"^json\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^```json\s*|^```", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"```$", "", text.strip())
    return text.strip()

def extract_message_text(ai_message):
    # LangChain AIMessage objects have a .content attribute
    return getattr(ai_message, "content", str(ai_message))

# providing some previous chats for better recommendations
def format_history(messages, n=4):
    history = messages[-n*2:] if len(messages) >= n*2 else messages
    history_str = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"
    return history_str


@st.cache_resource
def get_suggestion_chain():
    schema = get_schema_details()
    def build_prompt(inputs):
        return suggestion_prompt.format(schema=schema, question=inputs["question"])
    chain = (
            RunnableLambda(build_prompt) 
            | llm 
            | RunnableLambda(extract_message_text)
            | RunnableLambda(clean_json_output) 
            | json_parser
    )
    return chain

def get_followup_suggestions(question):
    chain = get_suggestion_chain()
    return chain.invoke({"question": question})
