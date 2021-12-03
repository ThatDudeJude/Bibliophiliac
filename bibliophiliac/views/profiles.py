from flask import Blueprint, render_template, redirect, flash
from flask.globals import request, g, current_app, session
from flask.helpers import flash, url_for
from sqlalchemy.exc import ArgumentError
# from werkzeug.utils import secure_filename
from bibliophiliac.views.database import access_database
from bibliophiliac.views.authentication import check_user_permission 
import os, imghdr



bp = Blueprint('profile', __name__) 
basedir = os.path.abspath(os.path.dirname(__name__))                

@bp.route('/profile/<string:name>')
@check_user_permission
def user_profile(name):

    can_edit = False
    user_name = name
    db = access_database()
    error = None
    if name == g.get('username', None):
        try:
            reviews = db.execute("SELECT * FROM reviews JOIN books ON books.isbn=reviews.book_isbn WHERE name_id=:id", {"id": g.id}).fetchall()
            can_edit = True
        except ArgumentError:
            error = "Invalid Request"
    elif name:
        try:            
            reviews = db.execute("SELECT * FROM users JOIN reviews ON reviews.name_id=users.id JOIN books ON books.isbn=reviews.book_isbn WHERE name=:name", {"name": name}).fetchall()
                        
        except ArgumentError:
            error = "Invalid Request!"
    
    if error:
        flash(error)
        return render_template('error.html'), 404
    else:
        total_reviews = len(reviews)
        total_ratings = 0
        avg_rating = 0            
        if total_reviews:
            for review in reviews:
                total_ratings += int(review.rating)
            avg_rating = total_ratings/total_reviews
    if os.path.exists(os.path.join(basedir + current_app.config['AVATARS_FOLDER'], name)):
        img = f'imgs/avatars/{name}'
    else:
        img = 'imgs/Background6.png'
                                   
    return render_template('reviews/profile.html', reviews=reviews, total_reviews=total_reviews, avg_rating=avg_rating, can_edit=can_edit, username=user_name, img=img)
    

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
            replace_name = request.form.get('new_name')            
            if g.username != replace_name:
                db.execute('UPDATE users SET name=:name WHERE id=:id', {"name": replace_name, "id":id})
                db.commit()                
                session['user_name'] = replace_name
                g.username = replace_name
            ext = os.path.splitext(file.filename)[1]
            allowed_ext = ['.jpg', '.jpeg', '.png', '.gif']
            if validate_avatar(file.stream) == ext and ext in allowed_ext:                                
                file.save(os.path.join(basedir + current_app.config['AVATARS_FOLDER'], g.username))                                        
        except ArgumentError:
            flash(f'Something went Wrong!{file}')
            return render_template('error.html'), 422                                   
    return redirect(url_for('profile.user_profile', name=g.username))
