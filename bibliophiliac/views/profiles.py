from flask import Blueprint, render_template, redirect, flash
from flask.globals import request, g, current_app, session
from flask.helpers import flash, url_for
from sqlalchemy.exc import IntegrityError, ArgumentError
from bibliophiliac.views.database import access_database
from bibliophiliac.views.authentication import check_user_permission
import os, imghdr, requests, glob
from bibliophiliac.views.search_and_reviews import fetch_from_api
from .search_and_reviews import find_profile_image


bp = Blueprint("profile", __name__)
basedir = os.path.abspath(os.path.dirname(__name__))


def search_books_image(books_results):
    api_data = []
    for result in books_results:
        try:
            res = requests.get(
                "https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key=AIzaSyDniynUGFYHQi2ooiC-Q9G9PUDvu-TKVbY".format(
                    result.isbn
                )
            )
            data = res.json()
            books_data = data["items"][0]["volumeInfo"]
            api_data.append({"image": books_data["imageLinks"]["thumbnail"]})
        except:
            api_data.append(
                {"image": url_for("static", filename="imgs/Background6.png")}
            )
    books_results = zip(books_results, api_data)
    return books_results


@bp.route("/profile/<string:name>", methods=["GET"])
@check_user_permission
def show_user_profile(name):
    if request.method == "GET":
        can_edit = False
        user_name = name
        file = find_profile_image(user_name)
        _, extension = os.path.splitext(file)
        profile_image = user_name + extension
        db = access_database()
        error = None
        if name == g.get("username", None):
            try:
                logged_in_user_reviews = db.execute(
                    "SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id",
                    {"id": g.id},
                ).fetchall()
                review_stats = db.execute(
                    "WITH review_stats AS (SELECT name_id, COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews GROUP BY name_id) SELECT * FROM review_stats WHERE name_id=:id",
                    {"id": g.id},
                ).fetchone()
                user_reviews = logged_in_user_reviews
                can_edit = True
            except ArgumentError:
                error = "Invalid Request"
        elif name:
            try:
                user_reviews = db.execute(
                    "SELECT * FROM users JOIN reviews ON reviews.name_id=users.id JOIN books ON books.isbn=reviews.book_isbn WHERE name=:name",
                    {"name": name},
                ).fetchall()
                review_stats = db.execute(
                    "WITH review_stats AS (SELECT name_id, COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews GROUP BY name_id) SELECT * FROM review_stats JOIN users ON users.id=name_id WHERE users.name=:name",
                    {"name": name},
                ).fetchone()

            except ArgumentError:
                error = "Invalid Request!"

        if error:
            flash(error)
            return render_template("error.html"), 404
        elif user_reviews is not None and user_reviews != []:
            user_reviews = zip(
                user_reviews, [fetch_from_api(book.isbn) for book in user_reviews]
            )

        return render_template(
            "reviews/profile.html",
            user_reviews=user_reviews,
            review_stats=review_stats,
            can_edit=can_edit,
            username=user_name,
            profile_image=profile_image,
        )


def validate_avatar(file_stream):
    header = file_stream.read(512)
    file_stream.seek(0)
    format = imghdr.what(None, header)
    if format:
        return "." + (format if format != "jpeg" else "jpg")
    else:
        return None


def find_profile_image(filename):
    file = [
        file
        for file in glob.glob(
            os.path.join(basedir + current_app.config["AVATARS_FOLDER"], filename + "*")
        )
    ][0]
    return file


@bp.route("/profile/update/<int:id>", methods=["GET", "POST"])
@check_user_permission
def update_profile(id):
    if request.method == "POST":
        current_app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000
        try:
            db = access_database()
            file = request.files["avatar_photo"]
            replacing_name = request.form.get("new_name")
            oldname = g.username
            if g.username != replacing_name:
                db.execute(
                    "UPDATE users SET name=:name WHERE id=:id",
                    {"name": replacing_name, "id": id},
                )
                db.commit()
                session["user_name"] = replacing_name
                g.username = replacing_name
            if file.filename:
                extension = os.path.splitext(file.filename)[1]
                allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]
                if (
                    validate_avatar(file.stream) == extension
                    and extension in allowed_extensions
                ):
                    image_file = find_profile_image(oldname)
                    os.remove(image_file)
                    file.save(
                        os.path.join(
                            basedir + current_app.config["AVATARS_FOLDER"],
                            g.username + extension,
                        )
                    )
            elif oldname != g.username:
                file = find_profile_image(oldname)
                avatar, extension = os.path.splitext(file)
                os.rename(
                    os.path.join(
                        basedir + current_app.config["AVATARS_FOLDER"],
                        oldname + extension,
                    ),
                    os.path.join(
                        basedir + current_app.config["AVATARS_FOLDER"],
                        g.username + extension,
                    ),
                )
        except IntegrityError:
            flash(f"Username {g.username} already exists!")
        return redirect(url_for("profile.show_user_profile", name=g.username))
