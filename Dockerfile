
FROM python:3.10-bullseye as builder
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool
ARG TARGETPLATFORM

RUN apt-get update && apt-get install -y \
    build-essential \
    librdkafka1 \
    librdkafka-dev

COPY requirements.txt* .
RUN \ 
  case ${TARGETPLATFORM} in \
    "linux/amd64")  REQ_FILE="requirements.txt"  ;; \
    "linux/arm64") REQ_FILE="requirements.txt.arm64"  ;; \
  esac && \
  pip install --root="/install" -r $REQ_FILE

# runtime
FROM python:3.10-slim-bullseye
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool
ARG TARGETPLATFORM

RUN \
  if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
    apt-get update && apt-get install -y librdkafka1 ; \
  fi  
USER 3001:3001


COPY --from=builder /install /
COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000