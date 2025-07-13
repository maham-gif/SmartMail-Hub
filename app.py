from flask import Flask, render_template, request, redirect, session, url_for
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-very-secret-key"

USERS_FILE = "data/users.json"
EMAILS_FILE = "data/emails.json"

def load_users():
    return json.load(open(USERS_FILE))

def load_emails():
    return json.load(open(EMAILS_FILE))

def save_emails(emails):
    json.dump(emails, open(EMAILS_FILE, "w"), indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form["user_id"]
        pwd = request.form["password"]
        users = load_users()
        if uid in users and users[uid] == pwd:
            session["user"] = uid
            return redirect(url_for("inbox"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/inbox")
def inbox():
    if "user" not in session:
        return redirect(url_for("login"))
    emails = load_emails()
    my_emails = [e for e in emails if e["to"] == session["user"] or e["from"] == session["user"]]
    return render_template("inbox.html", emails=my_emails, me=session["user"])

@app.route("/compose", methods=["GET", "POST"])
def compose():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        to = request.form["to"]
        subj = request.form["subject"]
        body = request.form["body"]
        emails = load_emails()
        new = {
            "id": str(uuid.uuid4()),
            "from": session["user"],
            "to": to,
            "subject": subj,
            "body": body,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        emails.append(new)
        save_emails(emails)
        return redirect(url_for("inbox"))
    return render_template("compose.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
