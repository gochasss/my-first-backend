from datetime import date
import os
print("TEMPLATES:", os.listdir("templates"))

from flask import Flask, request, redirect, session, render_template
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret123"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as db:
            user = db.execute(
                "SELECT id FROM users WHERE username=? AND password=?",
                (username, password)
            ).fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/tasks")

    return render_template("index.html")



# ---------- DATABASE ----------

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                user_id INTEGER,
                is_main INTEGER DEFAULT 0
            )
        """)

def migrate():
    with get_db() as db:
        try:
            db.execute("ALTER TABLE tasks ADD COLUMN day TEXT")
        except:
            pass

init_db()
migrate()

# ---------- AUTH ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as db:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )

        return redirect("/")

    return render_template("register.html")
# ---------- TASKS ----------

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    today = date.today().isoformat()

    if request.method == "POST":
        text = request.form["task"]
        is_main = 1 if "main" in request.form else 0

        with get_db() as db:
            if is_main:
                db.execute("UPDATE tasks SET is_main=0 WHERE user_id=?", (user_id,))
            db.execute(
                "INSERT INTO tasks (text, user_id, is_main, day) VALUES (?, ?, ?, ?)",
                (text, user_id, is_main, today)
            )

    with get_db() as db:
        rows = db.execute(
            "SELECT id, text, is_main FROM tasks WHERE user_id=? AND day=?",
            (user_id, today) 
        ).fetchall()

    return render_template("tasks.html", rows=rows)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" not in session:
        return redirect("/")

    with get_db() as db:
        db.execute(
            "DELETE FROM tasks WHERE id=? AND user_id=?",
            (task_id, session["user_id"])
        )

    
    return redirect("/tasks")


# ---------- RUN ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
