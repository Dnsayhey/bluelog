from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap4()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
