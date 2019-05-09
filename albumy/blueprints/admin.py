from flask import Blueprint, flash, render_template
from wtforms import StringField, BooleanField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email
from albumy.models import User, Role
from albumy.decorators import permission_required
from albumy.utils import redirect_back
from albumy.forms.user import EditProfileForm
from albumy.extensions import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/index')
def index():
    return 'admin'


@admin_bp.route('/lock/user/<int:user_id>')
@permission_required('MODERATE')
def lock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.lock()
    flash('Account locked.', 'info')
    return redirect_back()


@admin_bp.route('/unlock/user/<int:user_id>')
@permission_required('MODERATE')
def unlock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unlock()
    flash('Account unlocked.', 'info')
    return redirect_back()


@admin_bp.route('/block/user/<int:user_id>')
@permission_required('MODERATE')
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.block()
    flash('Account blocked.', 'info')
    return redirect_back()


@admin_bp.route('/unblock/user/<int:user_id>')
@permission_required('MODERATE')
def unblock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unblock()
    flash('Account unblocked.', 'info')
    return redirect_back()


class EditProfileAdminForm(EditProfileForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    role = SelectField('Role', coerce=int)
    active = BooleanField('Active')
    confirmed = BooleanField('Confirmed')
    submit = SubmitField()

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('The email; si already in use.')


@admin_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@permission_required('MODERATE')
def edit_profile_admin(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        role = Role.query.get(form.role.data)
        if role.name == 'Locked':
            user.lock()
        user.role = role
        user.bio = form.bio.data
        user.confirmed = form.confirmed.data
        user.active = form.active
        user.location = form.location.data
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect_back()
    form.name.data = user.name
    form.role.data = user.role
    form.bio.data = user.bio
    form.website = user.website
    form.location = user.location
    form.username = user.username
    form.email = user.email
    form.confirmed.data = user.confirmed
    form.active.data = user.active
    return render_template('admin/edit_profile.html', form=form, user=user)


