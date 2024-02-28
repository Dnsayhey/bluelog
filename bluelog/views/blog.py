from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user

from bluelog import db
from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.forms import AdminCommentForm, CommentForm
from bluelog.models import Category, Comment, Post
from bluelog.utils import redirect_back

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("BLUELOG_POST_PER_PAGE", 10)

    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    posts = pagination.items

    return render_template(
        "blog/index.html",
        pagination=pagination,
        posts=posts,
    )


@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("BLUELOG_POST_PER_PAGE", 10)
    pagination = (
        Post.query.with_parent(category)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=per_page)
    )
    posts = pagination.items
    return render_template(
        "blog/category.html",
        category=category,
        pagination=pagination,
        posts=posts,
    )


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get("page", 1, int)
    per_page = current_app.config.get("BLUELOG_COMMENT_PER_PAGE", 20)
    pagination = (
        Comment.query.with_parent(post)
        .filter_by(reviewed=True)
        .order_by(Comment.timestamp.asc())
        .paginate(page=page, per_page=per_page)
    )
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config["BLUELOG_EMAIL"]
        form.site.data = url_for("blog.index")
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        if not post.can_comment:
            abort(400)
        comment = Comment(
            author=form.author.data,
            body=form.body.data,
            email=form.email.data,
            site=form.site.data,
            from_admin=from_admin,
            reviewed=reviewed,
            post_id=post_id,
        )
        replied_comment_id = request.args.get("reply")
        if replied_comment_id:
            replied_comment = Comment.query.get_or_404(replied_comment_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)

        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash("Comment published.", "info")
        else:
            flash("Thanks, your comment will be published after reviewed.", "info")
            send_new_comment_email(post)
        return redirect(url_for("blog.show_post", post_id=post_id))

    return render_template(
        "blog/post.html", post=post, pagination=pagination, comments=comments, form=form
    )


@blog_bp.route("/about")
def about():
    return render_template("blog/about.html")


@blog_bp.route("/reply/comment/<int:comment_id>")
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash("Comment disabled.", "warning")
    return redirect(
        url_for(
            "blog.show_post",
            post_id=comment.post_id,
            reply=comment_id,
            author=comment.author,
        )
        + "#comment-form"
    )


@blog_bp.route("/change-theme/<theme_name>")
def change_theme(theme_name):
    if theme_name not in current_app.config["BLUELOG_THEMES"]:
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie("theme", theme_name, max_age=30 * 24 * 60 * 60)
    return response
