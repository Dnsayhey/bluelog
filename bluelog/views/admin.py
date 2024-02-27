from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from bluelog.extensions import db
from bluelog.forms import PostForm, SettingsForm
from bluelog.models import Category, Comment, Post
from bluelog.utils import redirect_back

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
@login_required
def login_protect():
    pass


@admin_bp.route("/settings", methods=["GET", "POST"])
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        print(request.form)
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash("Settings Updated.", "info")
        return redirect(url_for("admin.settings"))

    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about

    return render_template("admin/settings.html", form=form)


@admin_bp.route("/post/manage")
def manage_post():
    page = request.args.get("page", 1, int)
    per_page = current_app.config.get("BLUELOG_MANAGE_POST_PER_PAGE", 10)

    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    posts = pagination.items

    return render_template("admin/manage_post.html", pagination=pagination, posts=posts)


@admin_bp.route("/post/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        category = Category.query.get_or_404(form.category.data)
        title = form.title.data
        body = form.body.data

        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash("Post created.", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))
    return render_template("admin/new_post.html", form=form)


@admin_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        category = Category.query.get_or_404(form.category.data)
        title = form.title.data
        body = form.body.data

        post.title = title
        post.body = body
        post.category = category
        db.session.commit()
        flash("Post updated.", "success")
        return redirect(url_for("blog.show_post", post_id=post.id))

    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template("admin/new_post.html", form=form)


@admin_bp.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect_back()


@admin_bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect_back()


@admin_bp.route("/post/<int:post_id>/set_comment", methods=["POST"])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    post.can_comment = not post.can_comment
    db.session.commit()
    return redirect_back()
