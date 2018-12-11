import os

from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if valid_login(request.form['username'], request.form['password']):
            flash(" Successful logged in")
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = 'Incorrect username and password'
    return render_template('login.html', error=error)


@app.route("/welcome")
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))


def valid_login(username, password):
    if username == password:
        return True
    return False


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
