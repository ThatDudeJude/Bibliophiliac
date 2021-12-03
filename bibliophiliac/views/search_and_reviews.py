from flask import Blueprint, redirect, url_for
from flask.globals import request, g, session
from flask.helpers import flash
from flask.templating import render_template
from bibliophiliac.views.database import access_database

from bibliophiliac.views.authentication import check_user_permission 


bp = Blueprint('books', __name__) 


# def filter_search(db):
    


@bp.route('/search', methods = ['GET'])  
@check_user_permission # public books info first if not logged in
def search():    
    message = None
    search_results = None
    search = False 
    
    db = access_database()
    value = request.args.get('search_filter')
    search_query = request.args.get('search_term')
    if value:                                    
        sql = "SELECT * FROM books WHERE " + value + " ILIKE :term"
        search_results = db.execute(sql, {'term': f'%{search_query}%'}).fetchall()                        
        search = True
    elif search_query:
        search_results = db.execute("SELECT * FROM books WHERE isbn ILIKE :term OR "
            + "title ILIKE :term OR " + "author ILIKE :term OR " + "year ILIKE :term;", 
            {'term': f'%{search_query}%'}).fetchall()                        
        search = True
    if search_results == []:                        
        message = f"Search for '{request.args.get('search_filter', '')}: {search_query}' yielded 0 results.".capitalize()            

    return render_template('reviews/search.html', search=search, message=message, list_results=search_results)

@bp.route('/review/<string:isbn>')

def reviews(isbn):
    casual_user = False
    db = access_database()
    sql = "SELECT * FROM books WHERE isbn=:isbn_result"
    book_results = db.execute(sql, {'isbn_result': isbn}).fetchone()
    fetch_sql = "SELECT * FROM reviews JOIN users ON users.id=reviews.name_id WHERE book_isbn=:isbn_result"
    book_reviews = db.execute(fetch_sql, {'isbn_result': isbn}).fetchall()
    if g.get('id', None):
        user_sql = "SELECT * FROM reviews WHERE book_isbn=:isbn_result AND name_id=:id"
        review_exists = db.execute(user_sql, {'isbn_result': isbn, 'id':g.id }).fetchone()
    else:
        review_exists = casual_user 

    
        
    return render_template('reviews/book_reviews.html', result=book_results, book_reviews=book_reviews, user_review=review_exists )

    
@bp.route('/review/<string:isbn>', methods=["GET", "POST"])
@check_user_permission
def add_review(isbn):
    if request.method == 'POST':
        rating = request.form.get("rating")
        opinion =request.form.get("review_input")
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
        
    return redirect(url_for('books.reviews', isbn=isbn))


@bp.route('/your_reviews/<int:id>')            
@check_user_permission
def user_reviews(id):
    db = access_database()
    reviews = db.execute('SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id', {'id': id}).fetchall()
    message = None
    if reviews == []:
        message = "You hav no reviews yet"    

    return render_template('reviews/reviews_list.html', list_reviews=reviews, message=message, total=len(reviews))

@bp.route('/all_reviews')
def all_reviews():
    db = access_database()
    reviews = db.execute('SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn').fetchall()
    message = None
    if reviews == []:
        message = "You hav no reviews yet"    

    return render_template('reviews/reviews_list.html', list_reviews=reviews, message=message, total=len(reviews))