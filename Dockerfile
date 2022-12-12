FROM python:3.10-bullseye as base
FROM base as builder

run apt-get update && apt-get install -y \
    build-essential \
    librdkafka-dev

COPY requirements.txt .
RUN pip install --root="/install" -r requirements.txt

FROM base
COPY --from=builder /install /
COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000