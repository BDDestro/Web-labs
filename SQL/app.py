from flask import Flask, request, redirect, url_for, session, render_template
import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "ctf_users.db")

PORT = int(os.environ.get("PORT", "6001"))
SECRET_KEY = os.environ.get("SECRET_KEY", "gmit-sql-lab-secret")
FLAG = os.environ.get("CTF_FLAG", "GMIT{sql_1nj3ct10n_1s_3asy}")

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create a fresh local CTF database if it does not exist."""
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    existing = conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]

    if existing == 0:
        conn.executemany(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            [
                ("admin", "SuperSecretPassword9821!"),
                ("alice", "blue-moon-482"),
                ("bob", "coffee-lab-731"),
            ],
        )
        conn.commit()

    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    query_preview = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            error = "Username and password are required."
        else:
            # =============================================================
            # INTENTIONALLY VULNERABLE SQL QUERY FOR THIS LOCAL CTF LAB.
            # Never build real application queries this way.
            # =============================================================
            query = (
                "SELECT id, username FROM users "
                "WHERE username = '"
                + username
                + "' AND password = '"
                + password
                + "'"
            )

            query_preview = query

            try:
                conn = get_db()
                user = conn.execute(query).fetchone()
                conn.close()

                if user:
                    session["logged_in"] = True
                    session["username"] = user["username"]
                    return redirect(url_for("success"))

                error = "Invalid credentials!"

            except sqlite3.Error:
                # Keep the challenge beginner-friendly without exposing
                # internal filesystem/database details.
                error = "SQL query error. Check your injection syntax."

    return render_template(
        "home.html",
        error=error,
        query_preview=query_preview,
    )


@app.route("/success")
def success():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    return render_template(
        "success.html",
        flag=FLAG,
        username=session.get("username", "user"),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/reset")
def reset():
    session.clear()

    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_db()
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return {"status": "ok", "lab": "GMIT SQL Injection", "port": PORT}, 200


if __name__ == "__main__":
    init_db()

    print("=" * 62)
    print(" GMIT CTF - SQL INJECTION LAB")
    print("=" * 62)
    print(f"[+] Open: http://127.0.0.1:{PORT}/")
    print(f"[+] Reset: http://127.0.0.1:{PORT}/reset")
    print("[+] Test payload: admin' --")
    print("=" * 62)

    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
    )
