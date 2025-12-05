import os
import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request

from text_to_sql_core import generate_sql  # import your core logic

load_dotenv()

DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = int(os.getenv("MYSQL_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DB", "db_name")

app = Flask(__name__)


def execute_sql_query(sql_query: str):
   
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        cursorclass=pymysql.cursors.Cursor,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
    finally:
        conn.close()
    return columns, rows


@app.route("/", methods=["GET", "POST"])
def index():
    question = ""
    sql_query = ""
    columns = []
    rows = []
    error = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                sql_query = generate_sql(question)
                columns, rows = execute_sql_query(sql_query)
            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        question=question,
        sql_query=sql_query,
        columns=columns,
        rows=rows,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
