import logging
import os
from datetime import datetime

from flask import Flask, Response, flash, make_response, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from google.protobuf import json_format
from google.protobuf.json_format import ParseError
from wtforms.fields import HiddenField, SelectField, StringField, SubmitField
from wtforms.widgets import TextArea

import kafka

URL_PREFIX = "/bet"
COOKIE_NAME = "biznext-bet-group-id"
bootstrap_servers = os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
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
    duration = HiddenField("2.0")
    submit = SubmitField("Subscribe")


def static_file_content(filename: str) -> str:
    with open(f"./static/{filename}") as f:
        return f.read()


def pub_form(payload: str = ""):
    form = PublishForm()
    form.payload.data = payload
    return render_template("pub.html", form=form)


@app.route(URL_PREFIX + "/")
def root():
    return redirect(url_for("publish_page"))


@app.route(URL_PREFIX + "/pub")
def publish_page():
    return pub_form()


@app.route(URL_PREFIX + "/pub", methods=["POST"])
def handle_pub():
    form_keys = request.form.keys()
    if "sample" in form_keys:
        sample = static_file_content(request.form["topic"] + ".json")
        return pub_form(sample)
    elif "submit" in form_keys:
        topic = request.form["topic"]
        payload = request.form["payload"]
        try:
            log.info(f"publishing to {topic} on {bootstrap_servers}")
            message_pb = kafka.json2protobuf(topic, payload)
            kafka.produce(bootstrap_servers, topic, message_pb)
            log.info(f"published to {topic} on {bootstrap_servers}")
            flash(f"message published to topic {topic}", "success")
            return pub_form()
        except ParseError as e:
            flash(f"Error: {e}", "danger")
            return pub_form(payload)
    else:
        return None, 404


def consumer_group_id(request):
    return request.cookies.get(COOKIE_NAME) or f"bet-group-{int(datetime.now().timestamp())}"


def sub_form(group_id, messages: str = ""):
    form = SubscribeForm()
    form.messages.data = messages

    resp = make_response(render_template("sub.html", form=form))
    resp.set_cookie(COOKIE_NAME, group_id)
    log.info(f"sub_form: group_id={group_id}")
    return resp


@app.route(URL_PREFIX + "/sub")
def subscribe_page() -> Response:
    return sub_form(consumer_group_id(request))


@app.route(URL_PREFIX + "/sub", methods=["POST"])
def handle_sub():
    group_id = consumer_group_id(request)
    topic, duration, messages = request.form["topic"], request.form["duration"], ""

    for _, msg, timestamp in kafka.consume(bootstrap_servers, topic, group_id, float(duration)):
        messages += f"=== {type(msg)} at {timestamp.isoformat()} ===>\n"
        try:
            messages += json_format.MessageToJson(msg)
        except AttributeError:
            messages += str(msg)
        messages += "\n\n"

    return sub_form(group_id, messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
