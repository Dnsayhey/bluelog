import click
from flask import Flask

from bluelog.extensions import db
from bluelog.fakes import fake_admin, fake_categories, fake_comments, fake_posts
from bluelog.models import Admin, Category


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

    @app.cli.command()
    @click.option("--username", prompt=True, help="Username used to login.")
    @click.password_option("--password", prompt=True, help="Password used to login.")
    def init(username, password):
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo("Admin already exists, update admin...")
            admin.username = username
            admin.set_password(password)
        else:
            click.echo("Create admin...")
            admin = Admin(
                username="admin",
                blog_title="Bluelog",
                blog_sub_title="No, I'm the real thing.",
                name="Zero",
                about="This man is not lazy at all.",
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if Category is None:
            click.echo("Create default category...")
            category = Category(name="default")
            db.session.add(category)

        db.session.commit()
        click.echo("Done.")
