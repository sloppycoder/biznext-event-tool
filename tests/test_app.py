import pytest

import kafka
from app import URL_PREFIX, app, static_file_content


@pytest.fixture()
def client():
    return app.test_client()


def test_root_redirect_to_pub(client):
    response = client.get(f"{URL_PREFIX}/")
    assert response.status_code == 302 and response.headers["Location"] == f"{URL_PREFIX}/pub"


def test_handle_pub(client, mocker):
    topic = "instruction.command"
    json_str = static_file_content(f"{topic}.json")

    mocker.patch("kafka.produce", return_value=0)

    response = client.post(
        f"{URL_PREFIX}/pub",
        data={
            "topic": topic,
            "payload": json_str,
            "submit": "submit",
        },
    )

    assert response.status_code == 200
    kafka.produce.assert_called_once()


def test_handle_sub(client, mocker):
    topic = "instruction.command"

    mocker.patch("kafka.consume")

    response = client.post(
        f"{URL_PREFIX}/sub",
        data={
            "topic": topic,
            "duration": 0.1,
            "submit": "submit",
        },
    )

    assert response.status_code == 200
    kafka.consume.assert_called_once()
