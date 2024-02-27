import os

from flask import Flask

from bluelog.commands import register_commands
from bluelog.extensions import bootstrap, ckeditor, db, mail, moment, login_manager, csrf
from bluelog.models import Admin, Category, Link, Comment
from bluelog.settings import config
from bluelog.views.admin import admin_bp
from bluelog.views.auth import auth_bp
from bluelog.views.blog import blog_bp
from bluelog.views.errors import errors_bp


def register_blueprints(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(errors_bp)


def register_extensions(app: Flask):
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_template_context(app: Flask):
    @app.context_processor
    def inject_common_objects():
        admin = Admin.query.first()
        categories = Category.query.all()
        links = Link.query.all()
        unread_comments = Comment.query.filter_by(reviewed=False).count()
        return dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "dev")

    app = Flask("bluelog")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_template_context(app)

    return app
