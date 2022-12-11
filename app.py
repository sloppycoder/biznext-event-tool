import os

from flask import Flask, flash, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from google.protobuf.json_format import ParseError
from wtforms.fields import SelectField, StringField, SubmitField
from wtforms.widgets import TextArea

from kafka import TYPES_MAP, json2protobuf, produce

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

bootstrap = Bootstrap5(app)


class PublishForm(FlaskForm):
    topic = SelectField("Topic", choices=TYPES_MAP.keys())
    payload = StringField("Message (in JSON)", widget=TextArea())
    sample = SubmitField("Get Sample")
    submit = SubmitField("Publish")


def pub_form(payload: str = ""):
    form = PublishForm()
    form.payload.data = payload
    return render_template("pub.html", form=form)


def read_static_file(filename: str) -> str:
    with open(f"static/{filename}") as f:
        return f.read()


@app.route("/")
@app.route("/pub")
def publish_page():
    return pub_form()


@app.route("/pub", methods=["POST"])
def handle_pub():
    print(request.form)

    form_keys = request.form.keys()
    if "sample" in form_keys:
        sample_payload = read_static_file(request.form["topic"] + ".json")
        return pub_form(sample_payload)
    elif "submit" in form_keys:
        topic = request.form["topic"]
        payload = request.form["payload"]
        try:
            message = json2protobuf(topic, payload)
            produce(None, topic, message)
            flash(f"message published to topic {topic}", "success")
            return pub_form()
        except ParseError as e:
            flash(f"Error: {e}", "danger")
            return pub_form(payload)
    else:
        return "??", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
