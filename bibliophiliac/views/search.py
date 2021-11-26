from flask import Blueprint
from flask.globals import request, g, session
from flask.templating import render_template
from bibliophiliac.views.database import access_database

from bibliophiliac.views.authentication import check_user_permission 


bp = Blueprint('books', __name__) 


# def filter_search(db):
    


@bp.route('/search', methods = ['GET', 'POST'])  
@check_user_permission # public books info first if not logged in
def search():    
    message = None
    search_results = None
    if request.method == 'POST':        
        db = access_database()
        value = request.form.get('search_filter')
        search_query = request.form.get('search_term')
        if value:                                    
            sql = "SELECT * FROM books WHERE " + value + " ILIKE :term"
            search_results = db.execute(sql, {'term': f'%{search_query}%'}).fetchall()                        
        else:
            search_results = db.execute("SELECT * FROM books WHERE isbn ILIKE :term OR "
                + "title ILIKE :term OR " + "author ILIKE :term OR " + "year ILIKE :term;", 
                {'term': f'%{search_query}%'}).fetchall()                        

        if not search_results:                        
            message = "Search yielded no results."
    
    return render_template('reviews/search.html', messsage=message, list_results=search_results)


    