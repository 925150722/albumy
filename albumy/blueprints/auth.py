
from flask import Blueprint, url_for, redirect, flash, render_template
from flask_login import current_user, login_required, login_user, logout_user
from albumy.models import User
from albumy.extensions import db
from albumy.forms.auth import RegisterForm, ForgetPasswordForm, ResetPasswordForm, LoginForm
from albumy.settings import Operations
from albumy.emails import send_confirm_account_email, send_rest_password_email
from albumy.utils import generate_token, validate_token, redirect_back


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                login_user(user, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_account_email(user=user, token=token)
        flash('Confirm emails sent, check you inbox.', 'info')
        redirect('.login')
    return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('Account confirmed.', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/resend-confirmation')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect('main.index')

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_account_email(user=current_user, token=token)
    flash('New emails sent check your inbox.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index.html'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user=user, operation=Operations.CONFIRM)
            send_rest_password_email(user=user, token=token)
            flash('Password reset emails sent, check you inbox.', 'info')
            return redirect(url_for('.login'))
        flash('Invalid emails.', 'warning')
        return redirect(url_for('.forget_password'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None:
            return redirect(url_for('main.index'))
        if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=form.password.data):
            flash('Password update.', 'success')
            return redirect(url_for('.login'))
        else:
            flash('Invalid or expired token.', 'danger')
            return redirect('.forget_password')
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
