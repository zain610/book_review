import requests

from flask import Flask, session, render_template, request, redirect, url_for
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


@app.route("/", methods=["POST", "GET"])
def index():
    '''
    Main PAge of the web app. Here users will first see the homepage and decide what to do.
    :return: Index.html and process data to be showed on this page.
    '''
    isbn = []
    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "jUV1zj5KRLBJxzNzllbvQw", "isbns": "0441172717,0141439602"})
    print(res)
    try:
        username=session['username']
        print(username)
        return render_template("index.html", message=("Hello "+ username ))
    except KeyError:
        return render_template("index.html", message=("Hello, Please Login!"))


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
    '''
    Login is run when either:
    -> user clicks on login
    ->manually types url/login
    :return:
    -> Checks if username and password exists in db.
    -> Then Logs the username in a session.
    '''
    if request.method == 'POST':
        try:
            # THis scripts retrieves and then checks if the user exists in db
            username = request.form.get('username')
            password = request.form.get('password')
            print(username, password)

            '''
            fetch data 
            fetchone => to convert the resultproxy from db.execute to a tuple. mutable tuple

            '''
            data = db.execute(
                "Select (username, password) from authenticate where username=:username and password=:password",
                {"username": username, "password": password}).fetchone()
            print(data)
            if data:
                # store username inside session. to access later inside index.html. this shows that the user has logged in
                session["username"] = username
                return redirect(url_for('search'))
            return render_template('login.html')
        except ValueError:
            return render_template("error.html", message="Invalid credentials provided")
    return render_template('login.html')


#
@app.route("/search", methods=["POST", "GET"])
def search():
    '''
    Search page
    Take title, isbn, author name and output resutls

    :return:
    '''
    if request.method == "POST":
        try:
            session['username']
            keyword = str(request.form.get('keyword'))
            keyword = keyword.title()
            word = "%" + keyword + "%"
            print(word)
            # get title data
            title_data = db.execute(
                "Select * from book where title like (:keyword)",
                {"keyword": word}
            ).fetchall()
            print(type(title_data))
            # get isbn data
            isbn_data = db.execute(
                "Select * from book where isbn like (:isbn)",
                {"isbn": word}
            ).fetchall()
            print(isbn_data)
            # get author data
            author_data = db.execute(
                "Select * from book where author like (:author)",
                {"author": word}
            ).fetchall()
            print(author_data)
            return render_template("search.html", title_data = title_data, isbn_data = isbn_data, author_data = author_data)
        except KeyError:
            return render_template("index.html", message=("Hello, Please Login!"))
    return render_template("search.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/book/<isbn>", methods=["POST", "GET"])
def book(isbn):
    try:
        session['username']
        book = db.execute("Select * from book where isbn = :isbn", {"isbn": isbn}).fetchone()
        print(isbn, book)
        return render_template('/book.html', message=book)

    except KeyError:
        return render_template("index.html", message=("Hello, Please Login!"))


