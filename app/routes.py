from flask import render_template

from app import app

@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Mahdi"}
    posts = [
        {
            "author": {"username": "Bob"},
            "body": "What does six seven even mean?"
        },
        {
            "author": {"username": "Kid"},
            "body": "six seven, six seven, six seven, six seven, ..."
        }
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)
