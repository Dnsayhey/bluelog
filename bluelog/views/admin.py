from flask import Blueprint, render_template, flash, url_for, redirect, request

from flask_login import login_required, current_user

from bluelog.forms import SettingsForm
from bluelog.extensions import db

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