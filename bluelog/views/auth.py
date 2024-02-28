from flask import Blueprint, render_template, flash, redirect, url_for

from flask_login import login_user, logout_user, current_user, login_required

from bluelog.models import Admin
from bluelog.forms import LoginForm
from bluelog.utils import redirect_back

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if form.validate_on_submit():
        admin = Admin.query.first()
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        if admin is not None:
            if admin.username == username and admin.validate_password(password):
                login_user(admin, remember=remember)
                flash("Welcome back!", "info")
                return redirect_back()
            else:
                flash("Invalid username or password.", "warning")
        else:
            flash("No account.", "warning")
        
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout info.", "info")
    return redirect_back()
