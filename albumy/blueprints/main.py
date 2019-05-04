
import os
from flask import Blueprint, request, current_app, render_template, send_from_directory, flash, redirect, url_for, abort
from flask_dropzone import random_filename
from flask_login import login_required, current_user
from albumy.decorators import confirm_required, permission_required
from albumy.models import Photo
from albumy.extensions import db
from albumy.utils import resize_image


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return '1111'


@main_bp.route('/explore')
def explore():
    return 'explore'


@main_bp.route('/search')
def search():
    return 'search'


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@confirm_required
# @permission_required
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')
        filename = random_filename(f.filename)
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, 400)
        filename_m = resize_image(f, filename, 800)
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


@main_bp.route('/show_notifications/<filter>')
def show_notifications(filter):
    return 'show_notifications'


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)


@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('main/photo.html', photo=photo)


@main_bp.route('/phone/n/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo.id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        flash('This is already the last one.', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))


@main_bp.route('/phone/p/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo.id).order_by(Photo.id.asc()).first()
    if photo_p is None:
        flash('This is already the first one.', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))


@main_bp.route('/delete/photo/<int:photo_id>', methods=['POST'])
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo:
        abort(403)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo Deleted.', 'info')
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo.id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo.id).order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))
