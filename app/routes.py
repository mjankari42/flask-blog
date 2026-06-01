from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from app import app, db
from app.forms import LoginForm
from app.models import User


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Mahdi"}
    posts = [
        {"author": {"username": "Bob"}, "body": "What does six seven even mean?"},
        {
            "author": {"username": "Kid"},
            "body": "six seven, six seven, six seven, six seven, ...",
        },
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            select(User).where(User.username == form.username.data)
        )

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for("index"))

    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
