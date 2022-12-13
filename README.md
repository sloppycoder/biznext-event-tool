# BizNext Event Tool
Tools to publish and view messages in Kafka topics used by BizNext application.

## build container image
```
docker build -t ghcr.io/sloppycoder/biznext-event-tool:0.1.3 .

# use the following command on M1 Mac with Docker desktop or Rancher Desktop
docker buildx build --platform linux/amd64 -t ghcr.io/sloppycoder/biznext-event-tool:0.1.3 .

docker push  ghcr.io/sloppycoder/biznext-event-tool:0.1.3
```

## run kafka script locally
```
# run kafka script
export BOOTSTRAP_SERVERS=<your kafka brokers>

# publish a JSON file to the specified topic
# the message is publised as protobuf binary
python kafka.py instruction.command static/instruction.command.json

# liston on the default topic for 30s and print out messages
# if -f is specified at the end of the command, the script will run forever
python kafka.py consume instruction.command 

```

## run web app locally
```
python app.py

```

## Notes for development
### compile protobuf files into python
```
protoc -I ./protobuf/core_helper --python_out=./models/core_helper ./protobuf/core_helper/*.proto


```

### misc

This project is set up Python project with dev tooling pre-configured

* black
* flake8
* isort
* mypy
* VS Code support

## Setup
```
# create virtualenv
$ poetry shell

# install dependencies
(.venv)$ poetry install

```
