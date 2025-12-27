from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

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
                text TEXT NOT NULL,
                user_id INTEGER
            )
        """)

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
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

    return """
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br>
            <input name="password" placeholder="Password" type="password"><br>
            <button>Login</button>
        </form>
        <a href="/register">Register</a>
    """

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with get_db() as db:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?,?)",
                (username, password)
            )

        return redirect("/")

    return """
        <h2>Register</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br>
            <input name="password" placeholder="Password" type="password"><br>
            <button>Create account</button>
        </form>
    """

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    if request.method == "POST":
        text = request.form["task"]
        with get_db() as db:
            db.execute("INSERT INTO tasks (text, user_id) VALUES (?,?)", (text, user_id))

    with get_db() as db:
        rows = db.execute("SELECT text FROM tasks WHERE user_id=?", (user_id,)).fetchall()

    html = "<h2>Your tasks</h2>"
    html += "<form method='post'>"
    html += "<input name='task' placeholder='New task'>"
    html += "<button>Add</button></form><br>"

    for r in rows:
        html += f"<p>• {r[0]}</p>"

    html += "<br><a href='/logout'>Logout</a>"
    return html

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)