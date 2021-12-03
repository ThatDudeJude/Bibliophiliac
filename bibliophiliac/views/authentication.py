from flask import Blueprint 
from flask.globals import request, g, session
from flask import redirect, url_for, flash, render_template
from sqlalchemy.exc import IntegrityError
from bibliophiliac.views.database import access_database
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

bp = Blueprint('authenticate', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle the register request"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None 

        if not username :
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not error:
            db = access_database()
            try:
                db.execute("INSERT INTO users (name, password) VALUES (:username, :password)", {'username': username, 
                'password':generate_password_hash(password)})
                db.commit()
                return redirect(url_for('authenticate.login'))
            except IntegrityError:
                error = "Username already taken."
            
        flash(error)

    return render_template('log_auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle the login request"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None 

        if not username:
            error = 'Username required for logging'
            
        elif not password:
            error = 'Password required for logging'
        elif not error:
            db = access_database()            
            user = db.execute("SELECT * FROM users WHERE name=:name", {"name": username}).fetchone()
            
            if user and check_password_hash(user['password'], password): 
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                # return render_template('reviews/search.html')
                return redirect(url_for('books.search'))
            else:
                error = 'Wrong username and/or password.'
        flash(error)

    return render_template('log_auth/login.html')


@bp.route('/logout')
def logout():    
    if 'user_name' in session:        
        session.pop('user_id')
        session.pop('user_name')     
           
    return redirect(url_for('authenticate.login'))

@bp.before_app_request
def load_user_information():
    """Get user information and store it for every request duration"""
    if session.get('user_name', None):
        g.username = session['user_name']
        g.id = session['user_id']
        

def check_user_permission(view):
    """Check if user has priviledges to perform tasks"""
    @wraps(view)
    def wrapper(**kwargs):
        """Check if user information available, if not redirect to 
           login.  
        """
        if 'id' not in g:
            return redirect(url_for('authenticate.login'))
        return view(**kwargs)
    return wrapper 