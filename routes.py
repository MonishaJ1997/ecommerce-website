from app import app, db, login_manager
from flask import render_template, redirect, url_for, flash, request
from models import User
from forms import SignupForm, LoginForm
from flask_login import login_user, logout_user, login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials!", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
