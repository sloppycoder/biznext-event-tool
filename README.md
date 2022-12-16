# BizNext Event Tool
Tools to publish and view messages in Kafka topics used by BizNext application. Included are a script and simple Web UI that:

1. Use JSON as input to protobuf and publish to a topic
2. Consume messages from a topic, convert the protobuf messages to JSON



### run kafka script locally
```
# run kafka script
export BOOTSTRAP_SERVERS=<your kafka brokers>

# read json from a file and convert it to protobuf
# and publish to a topic

python kafka.py instruction.command static/instruction.command.json

# liston on the default topic and convert each message received into JSON.
# by default it will exit after running for 30s. if -f is specified at the 
# it will run forever, like tail -f 

python kafka.py consume instruction.command 

```

### run web app locally
```
export BOOTSTRAP_SERVERS=<your kafka brokers>
python app.py

# open your browser to http://localhost:5000
```

## Notes for developer
This project is set up Python project with dev tooling pre-configured

* black
* flake8
* isort
* mypy
* VS Code support

To start development, clone the repo and 
```
# poetry package manager is required

# start venv
poetry shell

# install dependencies
poetry install

# unit tests
pytest -s -v

# unit test with coverage report
ytest --cov=. -s -v

# compile proto files to python 
protoc -I ./protobuf/core_helper --python_out=./models/core_helper ./protobuf/core_helper/*.proto

# to build container image
docker build -t ghcr.io/<user>/biznext-event-tool:0.1.5 .

# to build on M1 Mac
docker buildx build --platform linux/amd64 -t ghcr.io/<user>/biznext-event-tool:0.1.5 .

# push the image to registry
docker push  ghcr.io/<user>/biznext-event-tool:0.1.5

# export poetry dependencies to requirements.txt
# required when building container images
poetry export --without-hashes --format=requirements.txt > requirements.txt

# export poetry dev dependencies to requirements-dev.txt
# required when running linting and unit tests on CI servers
poetry export --dev  --without-hashes --format=requirements.txt > requirements-dev.txt

```
