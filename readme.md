🚀 Text-to-SQL LLM Assistant

Natural Language → SQL Query → Executed Results
Built using LangChain, Gemini Flash, MySQL, Flask, and RAGAS.

📌 Overview

This project is an AI-powered Text-to-SQL Assistant that converts natural language questions into SQL queries using an LLM. The generated SQL is then executed on a live MySQL database, and the results are displayed through a clean Flask web interface.

It also includes a Jupyter Notebook demonstrating RAGAS-based evaluation of SQL query quality (Context Precision, Faithfulness, and Helpfulness).

✨ Features
🔹 1. LLM-generated SQL Queries

Converts natural language questions into valid MySQL SELECT statements

Uses Gemini 2.0 Flash via LangChain

Full schema-aware generation using dynamic prompt injection

Safety-checked to prevent UPDATE/DELETE/DROP/etc.

🔹 2. SQL Execution Engine

Executes generated SQL directly on a MySQL database

Returns:

Column names

Data rows

Query execution errors (if any)

🔹 3. Flask Web Interface

Clean UI to enter questions

Shows:

Generated SQL

Execution results

Error messages

Easy to deploy locally or on AWS EC2

🔹 4. RAGAS Evaluation Notebook

Included under /notebooks:

Evaluates SQL generation quality using:

Context Precision

Faithfulness

Helpfulness Score (Rubrics)

Uses Groq + HuggingFace embeddings

Helps measure model performance on SQL tasks

📂 Project Structure
text_to_sql_project/
│
├── app.py                   # Flask web server
├── text_to_sql_core.py      # LLM → SQL logic + schema injection
├── requirements.txt         
├── .gitignore
├── .env                     # (Not committed - contains API keys)
│
├── templates/
│   └── index.html           # Frontend UI
│
└── notebooks/
    └── evaluation_ragas.ipynb   # RAGAS evaluation & experiments

🛠️ Tech Stack

Languages & Frameworks

Python

Flask

LangChain

LLMs

Gemini 2.0 Flash

Groq llama-3.1-8b-instant (for evaluation)

Database

MySQL (via PyMySQL)

Evaluation

RAGAS

HuggingFace Embeddings

LangChain LLM wrappers

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/mayank-vk/text-to-sql-project.git
cd text-to-sql-project

2️⃣ Create .env file
GEMINI_API_KEY=your_key_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=text_to_sql

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask app
python app.py


Open your browser:

http://127.0.0.1:5000

🧠 How It Works (Architecture)

User enters question

Schema fetched dynamically from MySQL

Gemini LLM generates SQL using prompt template

SQL sanitized → must start with SELECT

SQL executed on MySQL using PyMySQL

Results displayed in browser

Evaluation notebook measures model quality with RAGAS

📊 Evaluation Example (RAGAS)

The notebook includes experiments measuring:

Context Precision

Helpfulness Score

Faithfulness

Sample output:

{
   "context_precision": 0.25,
   "helpfulness": 3.25
}

🎯 Future Enhancements

(optional section)

Add conversational memory

Add SQL query explanation using LLM

Support multiple databases (PostgreSQL, SQLite)

Add query caching for speed

Add chart visualizations (matplotlib)

📝 License

MIT License.

🙋 Author

Mayank v k
AI/ML Engineer | NLP | GenAI 