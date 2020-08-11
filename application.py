import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

#Set the secret key for maintaining user sessions
app.secret_key = 'This is a secret'

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

## home page
@app.route("/")
def index():
    print("In Index")
    return render_template("index.html")

## This route is called from search.html page, when user submits a request to search a book
## This will give the user all the books matching the criteria
@app.route("/search", methods=["POST","GET"])
def search():
    """Search a Book."""

    if 'username' not in session:
        return render_template("error.html", message="You are not logged in!")

    print ("In Search")
    isbn = request.form.get("s_isbn")
    title = request.form.get("s_title")
    author = request.form.get("s_author")

    print(f"Search book having {isbn}, {title}, {author}")          #for debug purpose
    books = []

    if isbn:
        t_isbn = '%'+isbn+'%'               #Create a pattern matching string, which can be used in sql
        sql = "SELECT * FROM books WHERE isbn LIKE (:isbn)"
        books_by_isbn = db.execute(sql, {"isbn": t_isbn})
        books += books_by_isbn;

    if title:
        t_title = '%'+title+'%'             #Create a pattern matching string, which can be used in sql
        sql = "SELECT * FROM books WHERE title LIKE (:title)"
        books_by_title = db.execute(sql, {"title": t_title})
        books += books_by_title;

    if author:
        t_author = '%'+author+'%'           #Create a pattern matching string, which can be used in sql
        sql = "SELECT * FROM books WHERE author LIKE (:author)"
        books_by_author = db.execute(sql, {"author": t_author})
        books += books_by_author;

    return render_template("search.html", books=books)

## This route is called from Search.html page when user clicks on title link.
## this will show the user the details and any reviews submitted by the users
## reviews will be fetch from reviews table
@app.route("/book/<int:book_id>")
def book(book_id):
    if 'username' not in session:
        return render_template("error.html", message="You are not logged in!")

    book_details = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    print (book_details)
    if book_details is None:
        return render_template("error.html", message="No such book exists")

    user = session['username']
    review_sql = "SELECT * FROM reviews JOIN users ON reviews.user_id = users.id WHERE users.username = :user AND reviews.book_id = :id"
    reviews = db.execute(review_sql, {"user": user, "id": book_id}).fetchall()

    isbn = book_details[1]
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
        params={"key": "your_access_key", "isbns": isbn})
## Data in json format
    data = res.json()
## extract the books list
    books = data["books"]
## extract the dictionary from first value
    result = books[0]
## extract the values by giving keys as Index
    avg_rating = result["average_rating"]
    rating_count = result["ratings_count"]

    return render_template("book.html", book=book_details, user=session['username'],
                                                    book_reviews = reviews, rating=avg_rating, count=rating_count)

## This route is called from index.html on click of "Register here" link
## This will take to user to registration.html page
@app.route("/registration")
def registration():
    """New User Registration."""
    print("In Registration")
    return render_template("registration.html", message = "")

## This route is called from registration page on submission of new user Registration
## It will first validate that the data is provided for both the fields
## It will validate if the user doesnt exists in the database
## IF the user is valid, it will redirect it to index page
@app.route("/validate_new_user", methods=["POST"])
def validate_new_user():
    """New user validation"""
    print("In Validate new user")
    user = request.form.get("r_name")
    password = request.form.get("r_password")

    if not user:
        return render_template("registration.html", message="Enter valid username or password")
    if not password:
        return render_template("registration.html", message="Enter valid username or password")

    if user and password:
        if (db.execute("SELECT * FROM users where username = :username",{"username": user}).rowcount > 0):
            return render_template("registration.html",message="User already exists")

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": user, "password": password})
        db.commit()
        return render_template("index.html", message="Registration Successful, login here")

## This route is called from index.html on submission of user credentials
## It will first validate that the data is provided for both the fields
## It will validate if the user exists in the database
## IF the user is valid, it will redirect it to search page
@app.route("/validate_user", methods=["POST"])
def validate_user():
    """User validation"""
    print("In Validate user")
    user = request.form.get("username")
    password = request.form.get("password")

    if not user:
        return render_template("index.html", message="Enter valid username or password")
    if not password:
        return render_template("index.html", message="Enter valid username or password")

    if user and password:
        if (db.execute("SELECT * FROM users where username = :username and password = :password",
                {"username": user, "password": password}).rowcount > 0):

                session['username'] = request.form['username']
                return redirect(url_for('search'))

        return render_template("index.html", message="Enter valid username or password")


##This route is called from book.html on submission of review by the user.
##User can submit only one review per book and the submitted review will be displayed back to user
##This function accepts book id
@app.route("/validate_review/<int:book_id>", methods=["POST"])
def validate_review(book_id):

    rating = request.form.get("s_rating")
    review = request.form.get("s_review")
    user = session['username']

    if rating or review:
        user_id = db.execute("SELECT id FROM users WHERE username = :username", {"username": user}).fetchone()
    #if comment from user already out there
        userid = user_id[0]
        print(userid)
        if (db.execute("SELECT * FROM reviews WHERE book_id = :book_id AND user_id = :user_id",
                {"book_id":book_id, "user_id":userid}).rowcount > 0):
                return redirect(url_for('book', book_id = book_id))

        db.execute("INSERT INTO reviews (rating, review, book_id, user_id) VALUES (:rating, :review, :book_id, :user_id)",
                    {"rating": rating, "review": review, "book_id": book_id, "user_id": userid})
        db.commit()

    return redirect(url_for('book', book_id = book_id))

## This route is when user clicks on logout link on each page.
## This will end the user session
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/api/<string:isbn>')
def book_api(isbn):
    """Return details about a single book based on isbn"""

    book_detail = db.execute("SELECT * FROM books where isbn = :isbn", {"isbn": isbn}).fetchone()

    if book_detail is None:
        return jsonify({"error": "Not Found"}), 404

    return jsonify({
            "title": book_detail.title,
            "author": book_detail.author,
            "publication_date": book_detail.publishyear,
            "isbn": book_detail.isbn
    })

@app.route('/api/review/<string:isbn>')
def review_api(isbn):
    """Return reviews about a single book based on isbn"""

    book_detail = db.execute("SELECT id FROM books where isbn = :isbn", {"isbn": isbn}).fetchone()
    book_id = book_detail[0]
    reviews = db.execute("SELECT * FROM reviews where book_id = :book_id", {"book_id": book_id}).fetchall()
    print (reviews)
    if reviews is None:
        return jsonify({"Message": "No reviews Found"})

## Need to change the below logic to return all the reviews for a particular book
    for review in reviews:
        rating = review.rating
        comment = review.review
        return jsonify({
            "rating": rating,
            "Comment": comment
    })
