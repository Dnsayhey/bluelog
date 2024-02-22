from flask import Blueprint, render_template, request, current_app

from bluelog.models import Admin, Category, Post

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("BLUELOG_POST_PER_PAGE", 10)

    admin = Admin.query.first()
    categories = Category.query.all()
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=per_page
    )
    posts = pagination.items

    return render_template(
        "blog/index.html",
        admin=admin,
        categories=categories,
        pagination=pagination,
        posts=posts,
    )


@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("BLUELOG_POST_PER_PAGE", 10)
    pagination = (
        Post.query.filter_by(category_id=category_id)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=per_page)
    )
    posts = pagination.items
    return render_template(
        "blog/category.html", category=category, pagination=pagination, posts=posts, categories=categories
    )


@blog_bp.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("blog/post.html", post=post)
