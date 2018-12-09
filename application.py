import requests

from datetime import timedelta
from flask import Flask, flash,session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template

DATABASE_URL = "postgres://stzunhlprsilqe:a3f1f9f217e9749383753f55b9a408c6582364ab75f2c36c5781537ee68aa577@ec2-50-17-203-51.compute-1.amazonaws.com:5432/demfabv2th1r11"
app = Flask(__name__)
# Check for environment variable
# if not os.environ[DATABASE_URL]:
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1)
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
    try:
        username=session['username']
        return render_template("index.html", message=("Hello "+ username ))
    except KeyError:
        return render_template("index.html", message=("Hello, Please Login!"))


@app.route("/register", methods=["POST", "GET"])
def register():
    '''
    Page for users to register.
    Input data is checked for if user exists in the db
    Then input data is stored into the db.

    :return:
    '''
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
        return render_template("index.html", message=("Hello, Please Login to access Search"))
    return render_template("search.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    '''
    Log people out of the page
    :return: removes username from session and returns user to the idnex page
    '''
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/book/<isbn>", methods=["POST", "GET"])
def book(isbn):
    '''
    Each user can enter, view and update their review and rating for a particular book.
    :param isbn: isbn input from url
    :return: page containing book dets, reviews by other users and input form for reviews.
    '''
    params = {
        'key': 'jUV1zj5KRLBJxzNzllbvQw',
        'isbns': isbn
    }
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params = params).json()
    gr_ratings_count = res['books'][0]['work_ratings_count']
    gr_average_rating = res['books'][0]['average_rating']
    gr_data = [gr_ratings_count, gr_average_rating]
    username = session['username']
    book = db.execute("Select * from book where isbn = :isbn", {"isbn": isbn}).fetchone()
    display_reviews = db.execute("Select username_review, review, rating from reviews where isbn_review = :isbn",
                                 {"isbn": isbn}).fetchall()
    review_by_username = db.execute("Select username_review from reviews where isbn_review = :isbn and username_review = :username",
                                    {"isbn": isbn, "username": username}).fetchall()
    average_rating = db.execute('Select AVG (rating) from reviews').fetchone()
    avg_rating = round(average_rating[0], 2)
    if request.form.get('review') is not None:
        if len(review_by_username) < 1:
            review = request.form.get('review')
            rating = request.form.get('rating')
            print(display_reviews, review, rating, username, average_rating)
            db.execute("Insert into reviews (username_review, isbn_review, review, rating) values (:username, :isbn, :review, :rating)", {"username": username, "isbn": isbn, "review": review, "rating": rating})
            db.commit()

    data = {
        'username': username,
        'book': book,
        'reviews': display_reviews,
        'avg_rating': avg_rating,
        'goodreads_data': gr_data,
    }
    # print(data)
    return render_template('/book.html', username = username, message=book, reviews=display_reviews, avg_rating = avg_rating, gr_data = gr_data)


@app.route("/api/<isbn>", methods=["POST","GET"])
def api(isbn):
    '''
    query retrieves relevant data from db
    :param isbn:
    :return: json object res
    '''
    data = db.execute("Select isbn, title, author, year_publication, count(review) as count_review, round(avg(rating), 2) as avg_rating from book b join reviews r on b.isbn = r.isbn_review where b.isbn=:isbn group by b.isbn, b.title, b.author, b.year_publication",
                      {"isbn": isbn}).fetchone()
    res = {
        "title": data.title,
        "author": data.author,
        "year": int(data.year_publication),
        "isbn": data.isbn,
        "review_count": data.count_review,
        "average_rating": int(data.avg_rating)
    }
    print(res)
    return jsonify(res)


