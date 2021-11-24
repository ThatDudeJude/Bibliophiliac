from flask import Blueprint
from flask.templating import render_template

from bibliophiliac.views.authentication import check_user_permission 


bp = Blueprint('books', __name__) 


@bp.route('/search')  
@check_user_permission # public books info first if not logged in
def search():    
    return render_template('reviews/search.html')


