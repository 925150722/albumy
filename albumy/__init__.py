
import os
import click
from flask import Flask
from albumy.blueprints.auth import auth_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.settings import config
from albumy.extensions import mail, moment, ckeditor, bootstrap, db, migrate, csrf, login_manager, dropzone, avatars
from albumy.models import Role


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')
    app.config.from_object(config[config_name])
    register_login(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_templates_context(app)
    register_errors(app)
    register_commends(app)
    return app


def register_login(app):
    pass


def register_extensions(app):
    mail.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')


def register_shell_context(app):
    pass


def register_templates_context(app):
    pass


def register_errors(app):
    pass


def register_commends(app):
    @app.cli.command()
    def init():
        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Done.')

    @app.cli.command()
    def init_db():
        db.drop_all()
        db.create_all()

