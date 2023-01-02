FROM python:3.10-slim-bullseye
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool "BizNext event tool"
ARG TARGETPLATFORM

COPY . .

RUN \
 if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
    apt update ; \
    apt install -y gcc libsasl2-2 libcurl4 ; \
    cp -r /platform/debian-aarch64/librdkafka/* /usr/local/. ; \
  fi ; \
  pip install -r requirements.txt


USER 3001:3001
ENV LD_LIBRARY_PATH /usr/local/lib
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000