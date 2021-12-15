from flask import Blueprint, render_template, redirect, flash
from flask.globals import request, g, current_app, session
from flask.helpers import flash, url_for
from sqlalchemy.exc import IntegrityError, ArgumentError,  UnsupportedCompilationError
# from werkzeug.utils import secure_filename
from bibliophiliac.views.database import access_database
from bibliophiliac.views.authentication import check_user_permission 
import os, imghdr



bp = Blueprint('profile', __name__) 
basedir = os.path.abspath(os.path.dirname(__name__))                

@bp.route('/profile/<string:name>', methods=['GET'])
@check_user_permission
def show_user_profile(name):
    if request.method == 'GET':
        can_edit = False
        user_name = name
        db = access_database()
        error = None    
        if name == g.get('username', None):
            try:
                logged_in_user_reviews = db.execute("SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id", {"id": g.id}).fetchall()
                user_reviews = logged_in_user_reviews
                can_edit = True
            except ArgumentError:
                error = "Invalid Request"
        elif name:
            try:            
                user_reviews = db.execute("SELECT * FROM users JOIN reviews ON reviews.name_id=users.id JOIN books ON books.isbn=reviews.book_isbn WHERE name=:name", {"name": name}).fetchall()
                            
            except ArgumentError:
                error = "Invalid Request!"
        
        if error:
            flash(error)
            return render_template('error.html'), 404
        else:
            total_reviews = len(user_reviews)
            total_ratings = 0
            average_rating_score = 0            
            if total_reviews:
                for review in user_reviews:
                    total_ratings += int(review.rating)
                average_rating_score = total_ratings/total_reviews        
                                   
        return render_template('reviews/profile.html', user_reviews=user_reviews, total_reviews=total_reviews, average_rating_score=average_rating_score, can_edit=can_edit, username=user_name)
    

def validate_avatar(file_stream):
    header = file_stream.read(512)
    file_stream.seek(0)
    format = imghdr.what(None, header)
    if format:
        return '.'+ (format if format != 'jpeg' else 'jpg')
    else:
        return None


@bp.route('/profile/update/<int:id>', methods=['GET', 'POST'])
@check_user_permission
def update_profile(id):
    if request.method == 'POST':
        current_app.config["MAX_CONTENT_LENGTH"] = 10 * 1000 * 1000        
        try:
            db = access_database()            
            file = request.files['avatar_photo']            
            replacing_name = request.form.get('new_name')            
            if g.username != replacing_name:
                db.execute('UPDATE users SET name=:name WHERE id=:id', {"name": replacing_name, "id":id})
                db.commit()
                os.unlink(os.path.join(basedir + current_app.config['AVATARS_FOLDER'], g.username))
                session['user_name'] = replacing_name
                g.username = replacing_name
            extension = os.path.splitext(file.filename)[1]
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if validate_avatar(file.stream) == extension and extension in allowed_extensions:                                
                file.save(os.path.join(basedir + current_app.config['AVATARS_FOLDER'], g.username))                                        
        except IntegrityError:
            flash(f'Username {g.username} already exists!')
            # return render_template('error.html'), 422                                   
    return redirect(url_for('profile.show_user_profile', name=g.username))
