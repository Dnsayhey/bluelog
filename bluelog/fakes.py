import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog.extensions import db
from bluelog.models import Admin, Category, Comment, Post, Link

fake = Faker()


def fake_admin():
    admin = Admin(
        username="admin",
        blog_title="Bluelog",
        blog_sub_title="No, I'm the real thing.",
        name="Zero",
        about="This man is not lazy at all.",
    )
    admin.set_password("adminpwd")
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name="Default")
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year(),
        )
        db.session.add(post)

    db.session.commit()


def fake_comments(count=500):
    admin = Admin.query.first()

    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year(),
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year(),
        )
        db.session.add(comment)

        comment = Comment(
            author=admin.name,
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year(),
        )
        db.session.add(comment)

    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year(),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
        )
        db.session.add(comment)

    db.session.commit()


def fake_links():
    links = [
        Link(name="Google", url="https://www.google.com"),
        Link(name="Baidu", url="https://www.baidu.com"),
        Link(name="Zero's Blog", url="https://zeronb.top"),
        Link(name="Zero's Watchlist", url="https://watchlist.zeronb.top"),
    ]
    db.session.add_all(links)
    db.session.commit()