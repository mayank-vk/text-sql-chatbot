import os
import re
from functools import lru_cache
from urllib.parse import quote_plus

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

FORBIDDEN_SQL = re.compile(
    r"\b("
    r"alter|call|create|delete|drop|execute|grant|insert|load_file|merge|"
    r"replace|revoke|truncate|update"
    r")\b|into\s+(out|dump)file",
    re.IGNORECASE,
)

PROMPT_TEMPLATE = """You are a careful MySQL text-to-SQL assistant.
Use only the provided schema. Return exactly one read-only SQL statement.
The statement must start with SELECT, must be valid MySQL, and must not include markdown, comments, explanation, or line breaks.

Schema:
{schema}

Question:
{question}

SQL Query:
"""


def get_mysql_uri() -> str:
    user = quote_plus(os.getenv("MYSQL_USER", "root"))
    password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    database = quote_plus(os.getenv("MYSQL_DB", "text_to_sql"))
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"


@lru_cache(maxsize=1)
def get_database() -> SQLDatabase:
    return SQLDatabase.from_uri(
        get_mysql_uri(),
        sample_rows_in_table_info=int(os.getenv("SCHEMA_SAMPLE_ROWS", "2")),
        lazy_table_reflection=True,
    )


def get_schema(_: dict | None = None) -> str:
    return get_database().get_table_info()


@lru_cache(maxsize=1)
def get_sql_chain():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file.")

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=api_key,
        temperature=0,
    )

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )


def clean_llm_sql(response: str) -> str:
    sql = response.strip()
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", sql, re.DOTALL | re.IGNORECASE)
    if fenced:
        sql = fenced.group(1).strip()
    return " ".join(sql.split())


def validate_select_sql(sql: str) -> str:
    normalized = clean_llm_sql(sql)
    without_trailing_semicolon = normalized[:-1].strip() if normalized.endswith(";") else normalized

    if not without_trailing_semicolon:
        raise ValueError("The model returned an empty SQL query.")
    if ";" in without_trailing_semicolon:
        raise ValueError("Blocked multiple SQL statements.")
    if not re.match(r"^\s*select\b", without_trailing_semicolon, re.IGNORECASE):
        raise ValueError(f"Blocked non-SELECT query: {without_trailing_semicolon}")
    if FORBIDDEN_SQL.search(without_trailing_semicolon):
        raise ValueError("Blocked unsafe SQL keyword in generated query.")

    return without_trailing_semicolon


def generate_sql(question: str) -> str:
    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    response = get_sql_chain().invoke({"question": question.strip()})
    return validate_select_sql(response)
