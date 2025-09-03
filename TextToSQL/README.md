# Text To SQL Chatbot

## Overview

This project is an AI-powered chatbot that converts natural language questions into SQL queries and executes them on a MySQL database. 
It uses LangChain, Cohere LLM, and Streamlit to provide an interactive UI for users to ask questions about their database and get answers instantly.

---

## Implementation Journey

### 1. Prototyping in Jupyter Notebook

- The project began with rapid prototyping in a Jupyter notebook [implementation.ipynb](implementation.ipynb).
- All core logic was tested here:
  - Connecting to the MySQL database.
  - Generating SQL queries from text using LangChain and Cohere.
  - Executing SQL queries and parsing results.
  - Building chains for multi-step reasoning.
  - Adding few-shot examples and dynamic schema selection.
  - Testing memory for follow-up questions.

### 2. Modular Python File Structure

After validating the workflow in the notebook, the code was refactored into modular Python files for maintainability and scalability:

- **`main.py`**: Streamlit UI for chat interaction.
- **`utils.py`**: Core chain construction, database connection, and chat history management.
- **`table_details.py`**: Table schema extraction and selection logic.
- **`prompts.py`**: Prompt templates and few-shot example selectors.
- **`examples.py`**: Example questions and queries for few-shot learning.
- **`.env`**: Environment variables for credentials and API keys.
- **`mysql_schema_description.csv`**: Table descriptions for dynamic schema selection.

---

## Features

- **Natural Language to SQL**: Ask questions in plain English, get SQL queries and answers.
- **Dynamic Table Selection**: Only relevant tables are included in prompts for concise and accurate SQL generation.
- **Few-Shot Learning**: Uses example queries to improve LLM performance.
- **Follow-Up Memory**: Remembers chat history for context-aware answers.
- **Streamlit UI**: User-friendly chat interface.

---

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/textToSql.git
   cd textToSql
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env` and fill in your MySQL credentials and API keys.
   - Example:
     ```
     db_user = "root"
     db_password = "yourpassword"
     db_host = "localhost"
     db_name = "classicmodels"
     COHERE_API_KEY = "your-cohere-key"
     LANGCHAIN_API_KEY = "your-langchain-key"
     ```

4. **Prepare your database**
   - Ensure your MySQL database is running and accessible.
   - Update `mysql_schema_description.csv` with your table descriptions if needed.

---

## Running the App

1. **Start the Streamlit UI**
   ```sh
   streamlit run main.py
   ```

2. **Interact with the chatbot**
   - Type your question in the chat box.
   - The bot will generate a SQL query, execute it, and return the answer.

---

## File Structure

```
textToSql/
│
├── main.py                      # Streamlit UI
├── utils.py                     # Chain logic and chat history
├── table_details.py             # Table schema selection
├── prompts.py                   # Prompt templates and example selectors
├── examples.py                  # Few-shot examples
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables
├── mysql_schema_description.csv # Table descriptions
└── implementation.ipynb         # Original notebook prototype
```

---

## Customization

- **Database**: Change `.env` and `mysql_schema_description.csv` for your own schema.
- **LLM**: Swap out Cohere for another LLM in `utils.py` and `table_details.py`.
- **Examples**: Add more few-shot examples in `examples.py` for better accuracy.
- 
---

## Credits

- Built with [LangChain](https://python.langchain.com/), [Cohere](https://cohere.com/), [Streamlit](https://streamlit.io/), and [Pandas](https://pandas.pydata.org/).
- Inspired by real-world business analytics and natural language interfaces for databases.

---

**Enjoy querying your database with natural language!**
