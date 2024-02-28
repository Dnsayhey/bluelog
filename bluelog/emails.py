from threading import Thread

from flask import current_app, url_for
from flask_mailman import EmailMessage


def _send_async_mail(app, message):
    with app.app_context():
        message.send()


def send_mail(subject, to, html):
    # app = current_app._get_current_object()
    # msg = EmailMessage(subject, html, to=[to])
    # msg.content_subtype = "html"
    # th = Thread(target=_send_async_mail, args=[app, msg])
    # th.start()
    # return th
    print("--- Send Email ---")
    print("--- To", to)
    print(html)
    print("------------------")


def send_new_comment_email(post):
    post_url = url_for("blog.show_post", post_id=post.id, _external=True) + "#comments"
    send_mail(
        subject="New comment",
        to=current_app.config["BLUELOG_EMAIL"],
        html="<p>New comment in post <i>%s</i>, click the link below to check:</p>"
        '<p><a href="%s">%s</a></P>'
        '<p><small style="color: #868e96">Do not reply this email.</small></p>'
        % (post.title, post_url, post_url),
    )


def send_new_reply_email(comment):
    post_url = (
        url_for("blog.show_post", post_id=comment.post_id, _external=True) + "#comments"
    )
    send_mail(
        subject="New reply",
        to=comment.email,
        html="<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>"
        '<p><a href="%s">%s</a></p>'
        '<p><small style="color: #868e96">Do not reply this email.</small></p>'
        % (comment.post.title, post_url, post_url),
    )
