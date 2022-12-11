from flask import Flask, render_template, request

from kafka import is_known_topic, json2protobuf, produce

app = Flask(__name__)


@app.route("/")
@app.route("/pub")
def publish_page():
    return render_template("pub.html")


@app.route("/pub/<topic>", methods=["POST"])
def publish_message(
    topic,
):
    if not is_known_topic(topic):
        return f"Unknown topic: {topic}", 404

    payload = request.data
    message = json2protobuf(topic, payload)
    produce(None, topic, message)

    return "published", 200


if __name__ == "__main__":
    app.run()
