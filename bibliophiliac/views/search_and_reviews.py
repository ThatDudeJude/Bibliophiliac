from flask import Blueprint, redirect, url_for
from flask.globals import request, g, session, current_app
from flask.helpers import flash
from flask.templating import render_template
from bibliophiliac.views.database import access_database
from bibliophiliac.views.authentication import check_user_permission
import requests
import os, shutil, glob

basedir = os.path.abspath(os.path.dirname(__name__))

bp = Blueprint("books", __name__)

api_key = None


def find_profile_image(filename):
    file = [
        file
        for file in glob.glob(
            os.path.join(basedir + current_app.config["AVATARS_FOLDER"], filename + "*")
        )
    ][0]
    return file


def fetch_from_api(isbn):
    global api_key
    if not api_key:
        api_key = current_app.config["BOOKS_API_KEY"]
    try:
        res = requests.get(
            "https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key={}".format(
                isbn, api_key
            ),
            timeout=30,
        )
        data = res.json()
        book_data = data["items"][0]["volumeInfo"]
        if "imageLinks" in book_data.keys():
            return {
                "average_rating": book_data["averageRating"],
                "total_reviews": book_data["ratingsCount"],
                "description": book_data["description"],
                "image": book_data["imageLinks"]["thumbnail"],
            }
        else:
            return {
                "average_rating": book_data["averageRating"],
                "total_reviews": book_data["ratingsCount"],
                "description": book_data["description"],
                "image": url_for("static", filename="imgs/default_book_image.png"),
            }
    except:
        return {
            "average_rating": "n/a",
            "total_reviews": "n/a",
            "description": "n/a",
            "image": url_for("static", filename="imgs/default_book_image.png"),
        }


def search_books_results_api(books_results):
    if books_results is not None and books_results != []:
        api_data = []
        api_data = []
        for result in books_results:
            try:
                res = requests.get(
                    "https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key={}".format(
                        result.isbn, api_key
                    ),
                    timeout=30,
                )
                data = res.json()
                books_data = data["items"][0]["volumeInfo"]
                api_data.append(
                    {
                        "description": books_data["description"],
                        "image": books_data["imageLinks"]["thumbnail"],
                    }
                )
            except:
                api_data.append(
                    {
                        "description": "n/a",
                        "image": url_for(
                            "static", filename="imgs/default_book_image.png"
                        ),
                    }
                )
        books_results = zip(books_results, api_data)
    return books_results


def search_book_info(isbn):
    try:
        res = requests.get(
            "https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key={}".format(
                isbn, api_key
            ),
            timeout=30,
        )
        data = res.json()
        book_data = data["items"][0]["volumeInfo"]
        google_books_data = {
            "average_rating": book_data["averageRating"],
            "total_reviews": book_data["ratingsCount"],
            "description": book_data["description"],
            "image": book_data["imageLinks"]["thumbnail"],
        }
    except:
        google_books_data = {
            "average_rating": "n/a",
            "total_reviews": "n/a",
            "description": "n/a",
            "image": url_for("static", filename="imgs/default_book_image.png"),
        }
    return google_books_data


def search_books_image(books_results):
    api_data = []
    for result in books_results:
        try:
            res = requests.get(
                "https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key={}".format(
                    result.isbn, api_key
                ),
                timeout=30,
            )
            data = res.json()
            books_data = data["items"][0]["volumeInfo"]
            api_data.append({"image": books_data["imageLinks"]["thumbnail"]})
        except:
            api_data.append(
                {"image": url_for("static", filename="imgs/default_book_image.png")}
            )
    books_results = zip(books_results, api_data)
    return books_results


@bp.route("/search", methods=["GET"])
@check_user_permission  # public books info first if not logged in
def search_for_book():
    message = None
    search_results = None
    is_successful = False

    db = access_database()
    search_filter = request.args.get("search_filter")
    search_query = request.args.get("search_term")
    if search_filter and search_query:
        sql_books_query = "SELECT * FROM books WHERE " + search_filter + " ILIKE :term"
        search_results = db.execute(
            sql_books_query, {"term": f"%{search_query}%"}
        ).fetchall()
        is_successful = True
    elif search_query:
        search_results = db.execute(
            "SELECT * FROM books WHERE isbn ILIKE :term OR "
            + "title ILIKE :term OR "
            + "author ILIKE :term OR "
            + "year ILIKE :term;",
            {"term": f"%{search_query}%"},
        ).fetchall()
        is_successful = True
    if search_results == [] or search_results is None:
        message = f"Search for '{request.args.get('search_filter', '')}: {search_query}' yielded 0 results.".capitalize()
    else:
        search_results = zip(
            search_results, [fetch_from_api(result.isbn) for result in search_results]
        )

    return render_template(
        "reviews/search.html",
        is_successful=is_successful,
        message=message,
        results_list=search_results,
    )


@bp.route("/review/<string:isbn>")
def find_review(isbn):
    db = access_database()
    sql_books_query = "SELECT * FROM books WHERE isbn=:isbn_result"
    book_results = db.execute(sql_books_query, {"isbn_result": isbn}).fetchone()
    book_stats = db.execute(
        "SELECT COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews WHERE book_isbn=:isbn",
        {"isbn": isbn},
    ).fetchone()
    sql_reviews_query = "SELECT * FROM reviews JOIN users ON users.id=reviews.name_id WHERE book_isbn=:isbn_result"
    book_reviews = db.execute(sql_reviews_query, {"isbn_result": isbn}).fetchall()
    print("book reviews", type(book_reviews))
    modified_book_reviews = []
    for review in book_reviews:
        print("Name", review["name"])
        review_column = dict(review)
        print("z", review_column)
        file = find_profile_image(review.name)
        avatar, extension = os.path.splitext(file)
        review_column["name"] = review.name
        review_column["profile_pic"] = review.name + extension
        print("name", review.name + extension, "avatar", avatar)
        # review.name = user_name + extension
        modified_book_reviews.append(review_column)

    if g.get("id", None):
        sql_review_query = (
            "SELECT * FROM reviews WHERE book_isbn=:isbn_result AND name_id=:id"
        )
        existing_user_review = db.execute(
            sql_review_query, {"isbn_result": isbn, "id": g.id}
        ).fetchone()
        login_user_review_exists = True if existing_user_review else False
    google_books_data = fetch_from_api(isbn)
    # print(data['items'][0]['volumeInfo']['imageLinks']['thumbnail'])
    return render_template(
        "reviews/book_reviews.html",
        book_results=book_results,
        book_reviews=modified_book_reviews,
        user_review_exists=login_user_review_exists,
        book_stats=book_stats,
        google_books=google_books_data,
    )


@bp.route("/review/<string:isbn>", methods=["GET", "POST"])
@check_user_permission
def add_review(isbn):
    if request.method == "POST":
        rating = request.form.get("rating")
        opinion = request.form.get("user_review")
        error = None
        if rating == "0":
            error = "Your rating is required!"
        elif not opinion:
            error = "Your review is required!"
        elif not all([int(g.id), int(isbn)]):
            error = "Invalid Request!"
        else:
            db = access_database()
            db.execute(
                "INSERT INTO reviews  (rating, opinion, name_id, book_isbn) VALUES (:rating, :opinion, :id, :isbn)",
                {"rating": rating, "opinion": opinion, "id": g.id, "isbn": isbn},
            )
            db.commit()

        flash(error)

    return redirect(url_for("books.find_review", isbn=isbn))


@bp.route("/your_reviews/<int:id>")
@check_user_permission
def fetch_user_reviews(id):
    db = access_database()
    reviews_list = db.execute(
        "SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id",
        {"id": id},
    ).fetchall()
    review_stats = db.execute(
        "WITH review_stats AS (SELECT name_id, COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews GROUP BY name_id) SELECT * FROM review_stats WHERE name_id=:id",
        {"id": id},
    ).fetchone()
    message = None
    if reviews_list == []:
        message = "You have no reviews yet"
        average_rating_score = None
    else:
        # reviews_list = search_books_image(reviews_list)
        reviews_list = zip(
            reviews_list, [fetch_from_api(book.isbn) for book in reviews_list]
        )
    return render_template(
        "reviews/my_reviews.html",
        reviews_list=reviews_list,
        message=message,
        review_stats=review_stats,
    )


@bp.route("/all_reviews")
def fetch_all_reviews():
    db = access_database()
    sql_query = "WITH all_reviews AS (SELECT book_isbn, COUNT(*) AS total_reviews, ROUND(AVG(rating),1) AS total_ratings FROM reviews GROUP BY book_isbn) SELECT * FROM books JOIN all_reviews ON all_reviews.book_isbn=books.isbn"
    reviews_list = db.execute(sql_query).fetchall()
    message = None
    total = len(reviews_list)
    if reviews_list == []:
        message = "No reviews added yet!"
    else:
        # reviews_list = search_books_image(reviews_list)
        reviews_list = zip(
            reviews_list, [fetch_from_api(book.isbn) for book in reviews_list]
        )

    return render_template(
        "reviews/all_reviews.html",
        reviews_list=reviews_list,
        message=message,
        total=total,
    )
