import pandas as pd
import streamlit as st
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from pydantic import BaseModel, Field
from langchain_cohere import ChatCohere
from langchain_core.runnables import RunnableLambda

llm = ChatCohere(model="command-r", temperature=0)
from typing import List

@st.cache_data
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("mysql_schema_description.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table_Name'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""
    table_name: List[str] = Field(description='Name of the table in SQL Database')

def get_tables(tables) -> List[str]:
    tables  = [table for table in tables.table_name]
    return tables


table_details = get_table_details()
table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = llm.with_structured_output(Table)
# not include "prompt_with_table_details_and_query"

select_table = (
    {"question": itemgetter("question")}
    | RunnableLambda(lambda x: f"{table_details_prompt}\n\nUser query: {x['question']}")
    | table_chain
    | RunnableLambda(get_tables)
)