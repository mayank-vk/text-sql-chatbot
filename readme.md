# Text-to-SQL LLM Assistant

Natural language -> SQL query -> executed database results.

Built with Python, Flask, LangChain, Gemini Flash, MySQL, RAGAS, Groq, and HuggingFace embeddings.

## Overview

This project is an AI-powered Text-to-SQL Assistant that converts natural language questions into SQL queries using an LLM. The generated SQL is validated as a single SELECT-only statement, executed against a live MySQL database, and displayed through a Flask web interface.

The notebook under `notebooks/` contains RAGAS-based evaluation experiments for SQL output quality, including context precision and helpfulness-style rubric scoring.

## Features

- Generates MySQL SELECT queries from natural language questions.
- Injects the live database schema into the LangChain prompt.
- Uses Gemini Flash through `langchain-google-genai`.
- Executes validated read-only SQL against MySQL through PyMySQL.
- Blocks non-SELECT statements, multiple statements, and unsafe SQL keywords before execution.
- Provides a lightweight Flask UI showing the question, generated SQL, results, and errors.
- Includes a RAGAS evaluation notebook using Groq and HuggingFace embeddings.

## Project Structure

```text
text-sql/
|-- app.py
|-- text_to_sql_core.py
|-- requirements.txt
|-- requirements-eval.txt
|-- .env.example
|-- templates/
|   `-- index.html
`-- notebooks/
    `-- text-to-sql.ipynb
```

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install app dependencies.

```bash
pip install -r requirements.txt
```

For the optional RAGAS notebook, install the evaluation stack separately. This is much larger because it includes HuggingFace and notebook dependencies.

```bash
pip install -r requirements-eval.txt
```

3. Create a local `.env` file from the example.

```bash
copy .env.example .env
```

4. Fill in your local API key and MySQL settings in `.env`.

```env
GEMINI_API_KEY=your_gemini_api_key_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DB=text_to_sql
```

5. Run the Flask app.

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## How It Works

1. The user enters a natural language question.
2. LangChain fetches the current MySQL schema.
3. Gemini Flash generates a single SQL query from the prompt.
4. The backend cleans and validates the query.
5. Only a single SELECT statement is allowed to execute.
6. Flask renders the generated SQL and query results.

## Evaluation

The notebook demonstrates a RAGAS workflow for benchmarking SQL-generation quality with Groq-hosted LLMs and HuggingFace embeddings. Example metrics include context precision and helpfulness-style rubric scores.

## Safety Notes

- Keep `.env` local. It is ignored by Git and should never be committed.
- The app validates generated SQL before execution, but it should still be used with a least-privilege MySQL user that has read-only permissions.
- Avoid using a production database for demos or experiments.

## Resume Summary

Built an end-to-end GenAI Text-to-SQL system using Flask, LangChain, Gemini Flash, and MySQL, with schema-aware prompt engineering, SELECT-only backend validation, live query execution, and a RAGAS evaluation pipeline using Groq and HuggingFace embeddings.
