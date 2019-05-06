
from flask import Blueprint, request, current_app, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from albumy.models import User, Photo, Collect
from albumy.decorators import confirm_required, permission_required
from albumy.utils import redirect_back


user_bp = Blueprint('user', __name__)


@user_bp.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Photo.query.with_parent(user).order_by(Photo.timestamp.desc()).paginate(page, per_page)
    photos = pagination.items
    return render_template('user/index.html', user=user, pagination=pagination, photos=photos)


@user_bp.route('/edit_profile')
def edit_profile():
    return 'edit_profile'


@user_bp.route('/<username>/collections')
def show_collections(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('user/collections.html', collects=collects, user=user, pagination=pagination)


@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
@confirm_required
@permission_required('FOLLOW')
def follow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        flash('Already followed.', 'info')
        return redirect(url_for('.index', username=username))
    current_user.follow(user)
    flash('User followed.', 'success')
    return redirect_back()


@user_bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        flash('Not follow yet.', 'info')
        return redirect_back(url_for('.index', username=username))
    current_user.unfollow(user)
    flash('User followed.', 'info')
    return redirect_back()


