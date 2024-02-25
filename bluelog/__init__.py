import os

import click
from flask import Flask

from bluelog.extensions import bootstrap, ckeditor, db, mail, moment
from bluelog.fakes import fake_admin, fake_categories, fake_comments, fake_posts
from bluelog.settings import config
from bluelog.views.admin import admin_bp
from bluelog.views.auth import auth_bp
from bluelog.views.blog import blog_bp
from bluelog.models import Admin, Category


def register_blueprints(app: Flask):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)


def register_extensions(app: Flask):
    bootstrap.init_app(app)
    ckeditor.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)


def register_template_context(app: Flask):
    @app.context_processor
    def inject_common_objects():
        admin = Admin.query.first()
        categories = Category.query.all()
        return dict(admin=admin, categories=categories)


def register_commands(app: Flask):

    @app.cli.command()
    @click.option(
        "--category", default=10, help="Quantity of categories, default is 10."
    )
    @click.option("--post", default=50, help="Quantity of posts, default is 50.")
    @click.option(
        "--comment", default=500, help="Quantity of comments, default is 500."
    )
    def forge(category, post, comment):
        """Forge: admin categories posts comments"""
        db.drop_all()
        db.create_all()

        fake_admin()
        fake_categories(category)
        fake_posts(post)
        fake_comments(comment)

        click.echo("Done!")


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
