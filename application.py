import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, escape
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_URL = "postgres://stzunhlprsilqe:a3f1f9f217e9749383753f55b9a408c6582364ab75f2c36c5781537ee68aa577@ec2-50-17-203-51.compute-1.amazonaws.com:5432/demfabv2th1r11"
app = Flask(__name__)
# Check for environment variable
# if not os.environ[DATABASE_URL]:
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

# GEt data from GoodReads API


@app.route("/")
def index():
    if 'username' in session:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "jUV1zj5KRLBJxzNzllbvQw", "isbns": ["1632168146", "3401063472"]})
        return render_template("index.html", message='Hey, {}!'.format(escape(session['username']), data = res.json()))
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    # Check if form is submitted
    if request.form.get('username') is None:
        return render_template("register.html")
    else:
        try:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            username = request.form.get('username')
            password = request.form.get('password')
        except ValueError:
            return render_template("error.html", message="Invalid credentials provided")

        # Check if the username exists
        if db.execute("Select * FROM authenticate where username= :username", {"username": username}).rowcount != 0:
            return render_template("error.html", message="This username exists, choose a new one")
        # Insert username, password into the database
        db.execute("Insert into authenticate values (:username, :password, :fname, :lname)",
                   {"username": username, "password": password, "fname": fname, "lname": lname})
        db.commit()
        return render_template("success.html", message="Successfully entered user into database")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.form.get('username') is None:
        return render_template("login.html")
    else:

        try:
            username = request.form.get('username')
            password = request.form.get('password')
        except ValueError:
            return render_template("error.html", message="Invalid credentials")

        if db.execute("Select (username, password) from authenticate where username=:username and password=:password",
                                        {"username": username, "password": password}):
            session['username'] = request.form['username']
            return redirect(url_for('index'))



@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('username')
    return redirect(url_for('index'))




