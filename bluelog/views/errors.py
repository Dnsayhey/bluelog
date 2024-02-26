from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(CSRFError)
def csrf_error(e):
    return render_template("errors/400.html", description=e.description), 400


@errors_bp.app_errorhandler(400)
def bad_request(e):
    return render_template("errors/400.html"), 400


@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404


@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500
