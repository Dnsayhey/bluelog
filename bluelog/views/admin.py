import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
)
from flask_login import current_user, login_required
from flask_ckeditor import upload_success, upload_fail

from bluelog.extensions import db
from bluelog.forms import CategoryForm, LinkForm, PostForm, SettingsForm
from bluelog.models import Category, Comment, Link, Post
from bluelog.utils import redirect_back, allowed_file

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
        flash("Post created.", "info")
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
        flash("Post updated.", "info")
        return redirect(url_for("blog.show_post", post_id=post.id))

    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template("admin/edit_post.html", form=form)


@admin_bp.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect_back()


@admin_bp.route("/comment/manage")
def manage_comment():
    filter_rule = request.args.get("filter", "all")
    page = request.args.get("page", 1, int)
    per_page = current_app.config.get("BLUELOG_COMMENT_PER_PAGE", 10)
    if filter_rule == "unread":
        query = Comment.query.filter_by(reviewed=False)
    elif filter_rule == "admin":
        query = Comment.query.filter_by(from_admin=True)
    else:
        query = Comment.query
    pagination = query.order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    comments = pagination.items

    return render_template(
        "admin/manage_comment.html", pagination=pagination, comments=comments
    )


@admin_bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect_back()


@admin_bp.route("/comment/<int:comment_id>/approve", methods=["POST"])
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.reviewed = True
    db.session.commit()
    flash("Comment published.", "info")
    return redirect_back()


@admin_bp.route("/post/<int:post_id>/set_comment", methods=["POST"])
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash("Comment disabled.", "info")
    else:
        post.can_comment = True
        flash("Comment enabled.", "info")
    db.session.commit()
    return redirect_back()


@admin_bp.route("/link/new", methods=["GET", "POST"])
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        flash("Link created.", "info")
        return redirect(url_for("blog.index"))

    return render_template("admin/new_link.html", form=form)


@admin_bp.route("/link/<int:link_id>/edit", methods=["GET", "POST"])
def edit_link(link_id):
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash("Link updated.", "info")
        return redirect(url_for("admin.manage_link"))

    form.name.data = link.name
    form.url.data = link.url
    return render_template("admin/edit_link.html", form=form)


@admin_bp.route("/link/manage")
def manage_link():
    return render_template("admin/manage_link.html")


@admin_bp.route("/link/<int:link_id>/delete", methods=["POST"])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("Link deleted.", "info")
    return redirect_back()


@admin_bp.route("/category/new", methods=["GET", "POST"])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category created.", "info")
        return redirect(url_for("blog.index"))

    return render_template("admin/new_category.html", form=form)


@admin_bp.route("/category/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("Category updated.", "info")
        return redirect(url_for("admin.manage_category"))
    form.name.data = category.name
    return render_template("admin/edit_category.html", form=form)


@admin_bp.route("/category/manage")
def manage_category():
    return render_template("admin/manage_category.html")


@admin_bp.route("/category/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category_id == 1:
        flash("You can not delete the default category.", "warning")
        return redirect_back()
    category.delete()
    flash("Category deleted.", "info")
    return redirect_back()


@admin_bp.route("/upload", methods=["POST"])
def upload_image():
    f = request.files.get("upload")
    if not allowed_file(f.filename):
        return upload_fail("Image only!")
    f.save(os.path.join(current_app.config["BLUELOG_UPLOAD_PATH"], f.filename))
    url = url_for(".get_image", filename=f.filename)
    return upload_success(url, f.filename)


@admin_bp.route("/uploads/<path:filename>")
def get_image(filename):
    return send_from_directory(
        current_app.config["BLUELOG_UPLOAD_PATH"], filename
    )
