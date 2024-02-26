import click
from flask import Flask

from bluelog import db
from bluelog.fakes import fake_admin, fake_categories, fake_comments, fake_posts


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
    @click.password_option("--password", prompt=True, help="Password user to login.")
    def init(username, password):
        pass
