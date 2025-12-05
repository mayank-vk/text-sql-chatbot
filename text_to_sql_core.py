import os
import re
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load env variables from .env
load_dotenv()

# ------------------ CONFIG -------------------
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DB", "text_to_sql")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY is not set in .env")

mysql_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)

db=SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=1)
context=db.get_table_info()

def get_schema(db):
    schema=db.get_table_info()
    return schema

template="""Based on the table schema below, write a SQL query that would answer the user's question:
Remember: Only provide me the sql query dont include anything else.Provide me the sql query in a single line dont add line breaks
Table schema: {schema}
Question: {question}
SQL Query:
"""

prompt=ChatPromptTemplate.from_template(template)

llm=ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    api_key=GEMINI_API_KEY)

sql_chain=(
    RunnablePassthrough.assign(schema=lambda _:get_schema(db))
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

def generate_sql(question: str) -> str:
    
    resp = sql_chain.invoke({"question": question}).strip()

    query = re.search(r"```sql\s*(.*?)```", resp, re.DOTALL | re.IGNORECASE)
    if query:
        resp = query.group(1).strip()

    # Enforce SELECT-only safety
    if not resp.upper().lstrip().startswith("SELECT"):
        raise ValueError(f"Blocked non-SELECT query: {resp}")

    return resp