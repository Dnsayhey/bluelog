import datetime
import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if sys.platform.startswith("win"):
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "++secret__key!!")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ECHO = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Bluelog Admin", MAIL_USERNAME)

    BLUELOG_EMAIL = os.getenv("BLUELOG_EMAIL")
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 20
    BLUELOG_COMMENT_PER_PAGE = 20
    BLUELOG_THEMES = {"perfect_blue": "Perfect Blue", "black_swan": "Black Swan"}
    BLUELOG_UPLOAD_PATH = os.path.join(basedir, "uploads")
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]

    # CKEDITOR_PKG_TYPE = "basic"
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=31)
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=31)


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, "bluelog-dev.sqlite")


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", prefix + os.path.join(basedir, "bluelog-prod.sqlite")
    )


if not os.path.exists(BaseConfig.BLUELOG_UPLOAD_PATH):
    os.mkdir(BaseConfig.BLUELOG_UPLOAD_PATH)

config = {"dev": DevelopmentConfig, "test": TestConfig, "prod": ProductionConfig}
