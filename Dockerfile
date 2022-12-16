
FROM python:3.10-bullseye as builder
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool

run apt-get update && apt-get install -y \
    build-essential \
    librdkafka-dev

COPY requirements.txt .
RUN pip install --root="/install" -r requirements.txt

# runtime
FROM python:3.10-slim-bullseye
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool
USER 3001:3001


COPY --from=builder /install /
COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000