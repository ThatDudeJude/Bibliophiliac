from flask import Blueprint, redirect, url_for
from flask.globals import request, g, session
from flask.helpers import flash
from flask.templating import render_template
from bibliophiliac.views.database import access_database
from bibliophiliac.views.authentication import check_user_permission
import requests

bp = Blueprint('books', __name__)

    
@bp.route('/search', methods = ['GET'])  
@check_user_permission # public books info first if not logged in
def search_for_book():    
    message = None
    search_results = None
    is_successful = False
    
    db = access_database()
    search_filter = request.args.get('search_filter')
    search_query = request.args.get('search_term')
    if search_filter and search_query:                                    
        sql_books_query = "SELECT * FROM books WHERE " + search_filter + " ILIKE :term"
        search_results = db.execute(sql_books_query, {'term': f'%{search_query}%'}).fetchall()                        
        is_successful = True
    elif search_query:
        search_results = db.execute("SELECT * FROM books WHERE isbn ILIKE :term OR "
            + "title ILIKE :term OR " + "author ILIKE :term OR " + "year ILIKE :term;", 
            {'term': f'%{search_query}%'}).fetchall()                        
        is_successful = True
    if search_results == []:                        
        message = f"Search for '{request.args.get('search_filter', '')}: {search_query}' yielded 0 results.".capitalize()            
    if search_results is not None and search_results != []:
        api_data = []
        for result in search_results:
            try:
                res = requests.get("https://www.googleapis.com/books/v1/volumes?q=+isbn:{}&maxResults=1&orderBy=newest&key=AIzaSyDniynUGFYHQi2ooiC-Q9G9PUDvu-TKVbY".format(result.isbn))
                data = res.json()
                book_data = data['items'][0]['volumeInfo']
                api_data.append({'avg': book_data['averageRating'], 'rating_avg':book_data['ratingsCount'], 'description': book_data['description'], 'image': book_data['imageLinks']['thumbnail']})
            except:
                api_data.append({'avg': 'n/a', 'rating_avg':"n/a", 'description': "n/a", 'image': url_for('static', filename='imgs/Background6.png')})
        search_results = zip(search_results, api_data)

    return render_template('reviews/search.html', is_successful=is_successful, message=message, results_list=search_results)

@bp.route('/review/<string:isbn>')

def find_review(isbn):    
    db = access_database()
    sql_books_query = "SELECT * FROM books WHERE isbn=:isbn_result"
    book_results = db.execute(sql_books_query, {'isbn_result': isbn}).fetchone()
    book_stats = db.execute("SELECT COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews WHERE book_isbn=:isbn", {'isbn': isbn}).fetchone()
    sql_reviews_query = "SELECT * FROM reviews JOIN users ON users.id=reviews.name_id WHERE book_isbn=:isbn_result"
    book_reviews = db.execute(sql_reviews_query, {'isbn_result': isbn}).fetchall()
    if g.get('id', None):
        sql_review_query = "SELECT * FROM reviews WHERE book_isbn=:isbn_result AND name_id=:id"
        existing_user_review = db.execute(sql_review_query, {'isbn_result': isbn, 'id':g.id }).fetchone()
        login_user_review_exists = True if existing_user_review else False
        
    return render_template('reviews/book_reviews.html', book_results=book_results, book_reviews=book_reviews, user_review_exists=login_user_review_exists, book_stats=book_stats )

    
@bp.route('/review/<string:isbn>', methods=["GET", "POST"])
@check_user_permission
def add_review(isbn):
    if request.method == 'POST':
        rating = request.form.get("rating")
        opinion =request.form.get("review-input")
        error = None
        if rating == '0':
            error = "Your rating is required!"
        elif not opinion:
            error = "Your review is required!"
        elif not all([int(g.id), int(isbn)]):
            error = "Invalid Request!"
        else:
            db = access_database()
            db.execute("INSERT INTO reviews  (rating, opinion, name_id, book_isbn) VALUES (:rating, :opinion, :id, :isbn)", 
                    {"rating": rating, "opinion": opinion, "id": g.id, "isbn": isbn})
            db.commit()                

        flash(error)
        
    return redirect(url_for('books.find_review', isbn=isbn))


@bp.route('/your_reviews/<int:id>')
@check_user_permission
def fetch_user_reviews(id):
    db = access_database()
    reviews_list = db.execute('SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id', {'id': id}).fetchall()    
    review_stats = db.execute('WITH review_stats AS (SELECT name_id, COUNT(*) AS total_reviews, ROUND(AVG(rating), 1) AS average_rating FROM reviews GROUP BY name_id) SELECT * FROM review_stats WHERE name_id=:id', {'id': id}).fetchone()
    message = None
    if reviews_list == []:
        message = "You have no reviews yet"    
        average_rating_score = None    
    
    return render_template('reviews/my_reviews.html', reviews_list=reviews_list, message=message, review_stats=review_stats)

@bp.route('/all_reviews')
def fetch_all_reviews():
    db = access_database()
    sql_query = "WITH all_reviews AS (SELECT book_isbn, COUNT(*) AS total_reviews, ROUND(AVG(rating),1) AS total_ratings FROM reviews GROUP BY book_isbn) SELECT * FROM books JOIN all_reviews ON all_reviews.book_isbn=books.isbn"
    reviews_list = db.execute(sql_query).fetchall()
    message = None
    total = len(reviews_list)
    if reviews_list == []:
        message = "No reviews added yet!"    
        
    return render_template('reviews/all_reviews.html', reviews_list=reviews_list, message=message, total=total)