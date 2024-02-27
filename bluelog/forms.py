from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    Email,
    URL,
    Optional,
)

from bluelog.models import Category


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 32)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Log in")


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("Name already in use.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField("Body", validators=[DataRequired()])
    category = SelectField("Category", coerce=int, default=1)
    submit = SubmitField("Post")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.id).all()
        ]


class CommentForm(FlaskForm):
    author = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    # email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 254)])
    email = StringField("Email", validators=[DataRequired(), Length(1, 254)])
    site = StringField("Site", validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField("Blog Title", validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField("Blog Sub Title", validators=[DataRequired(), Length(1, 100)])
    # about = CKEditorField("About", validators=[DataRequired()])
    about = TextAreaField("About", validators=[DataRequired()])
    submit = SubmitField("Save")


class LinkForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 60)])
    url = StringField("URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Save")
