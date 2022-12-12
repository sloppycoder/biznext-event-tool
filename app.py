import logging
import os

from flask import Flask, flash, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from google.protobuf.json_format import ParseError
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.widgets import TextArea

from kafka import TYPES_MAP, json2protobuf, produce

URL_PREFIX = "/bet"
bootstrap_servers = os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
bootstrap = Bootstrap5(app)
log = app.logger
log.setLevel(logging.INFO)


class PublishForm(FlaskForm):
    topic = SelectField("Topic", choices=TYPES_MAP.keys())
    payload = StringField("Message (in JSON)", widget=TextArea())
    sample = SubmitField("Get")
    submit = SubmitField("Publish")


def pub_form(payload: str = ""):
    form = PublishForm()
    form.payload.data = payload
    return render_template("pub.html", form=form)


def read_static_file(filename: str) -> str:
    with open(f"static/{filename}") as f:
        return f.read()


@app.route(URL_PREFIX + "/")
@app.route(URL_PREFIX + "/pub")
def publish_page():
    return pub_form()


@app.route(URL_PREFIX + "/pub", methods=["POST"])
def handle_pub():
    form_keys = request.form.keys()
    if "sample" in form_keys:
        sample_payload = read_static_file(request.form["topic"] + ".json")
        return pub_form(sample_payload)
    elif "submit" in form_keys:
        topic = request.form["topic"]
        payload = request.form["payload"]
        try:
            log.info(f"publishing to {topic} on {bootstrap_servers}")
            message = json2protobuf(topic, payload)
            ret = produce(bootstrap_servers, topic, message)
            if ret <= 0:
                log.info(f"published to {topic} on {bootstrap_servers}")
                flash(f"message published to topic {topic}", "success")
                return pub_form()
            else:
                log.info(f"producer.flus() return {ret}")
                flash(f"producer.flus() return {ret}", "danger")
        except ParseError as e:
            flash(f"Error: {e}", "danger")
            return pub_form(payload)
    else:
        return "??", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
