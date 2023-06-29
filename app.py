import logging
import os
from datetime import datetime

from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from google.protobuf import json_format
from google.protobuf.json_format import ParseError
from werkzeug.middleware.proxy_fix import ProxyFix
from wtforms.fields import BooleanField, SelectField, StringField, SubmitField
from wtforms.widgets import TextArea

import kafka

URL_PREFIX = "/bet"
COOKIE_NAME = "biznext-bet-group-id"
bootstrap_servers = os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092")

app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key if secret_key else os.urandom(32)
if os.environ.get("KUBERNETES_SERVICE_HOST"):
    print("running in kubernetes, using proxy fix")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

bootstrap = Bootstrap5(app)
log = app.logger
log.setLevel(logging.INFO)


class PublishForm(FlaskForm):
    topic = SelectField("Topic", choices=kafka.known_topics())
    payload = StringField("Message (in JSON)", widget=TextArea())
    sample = SubmitField("Get")
    submit = SubmitField("Publish")


class SubscribeForm(FlaskForm):
    topic = SelectField("Topic", choices=kafka.known_topics)
    messages = StringField("Messages (in JSON)", widget=TextArea(), render_kw={"readonly": True})
    reset_group_id = BooleanField("Start from beginning")
    submit = SubmitField("Subscribe")


def static_file_content(filename: str) -> str:
    with open(f"./static/{filename}") as f:
        return f.read()


@app.route(URL_PREFIX + "/pub")
def pub_page(payload: str = ""):
    form = PublishForm()
    form.payload.data = payload
    return render_template("pub.html", form=form)


@app.route(URL_PREFIX + "/")
def root():
    return redirect(url_for("pub_page"))


@app.route(URL_PREFIX + "/pub", methods=["POST"])
def handle_pub():
    form_keys = request.form.keys()
    if "sample" in form_keys:
        sample = static_file_content(request.form["topic"] + ".json")
        return pub_page(sample)
    elif "submit" in form_keys:
        topic = request.form["topic"]
        payload = request.form["payload"]
        try:
            log.info(f"publishing to {topic} on {bootstrap_servers}")

            message_pb = kafka.json2protobuf(topic, payload)
            if kafka.produce(bootstrap_servers, topic, message_pb) == 0:
                log.info(f"published to {topic} on {bootstrap_servers}")
                flash(f"message published to topic {topic}", "success")
            else:
                log.info(f"unable to publish to {topic} on {bootstrap_servers}")
                flash(f"message falied to publish to topic {topic}", "danger")

            return pub_page()
        except ParseError as e:
            flash(f"Error: {e}", "danger")
            return pub_page(payload)
    else:
        return None, 404


def new_group_id():
    return f"bet-group-{int(datetime.now().timestamp())}"


@app.route(URL_PREFIX + "/sub")
def sub_page(messages: str = "", group_id: str = ""):
    form = SubscribeForm()
    form.messages.data = messages
    form.reset_group_id.data = False

    resp = make_response(render_template("sub.html", form=form))
    if group_id != "":
        resp.set_cookie(COOKIE_NAME, group_id)
        log.info(f"sub_page: group_id={group_id}")

    return resp


@app.route(URL_PREFIX + "/sub", methods=["POST"])
def handle_sub():
    topic, reset_group_id = request.form["topic"], "reset_group_id" in request.form

    group_id = request.cookies.get(COOKIE_NAME)
    if group_id is None or reset_group_id:
        group_id = new_group_id()

    messages = ""
    for _, msg, timestamp in kafka.consume(bootstrap_servers, topic, group_id, 2.0):
        messages += f"=== {type(msg)} at {timestamp.isoformat()} ===>\n"
        try:
            messages += json_format.MessageToJson(msg)
        except AttributeError:
            messages += str(msg)
        messages += "\n\n"

    return sub_page(messages, group_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
