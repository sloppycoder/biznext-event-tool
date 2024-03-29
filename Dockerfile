FROM python:3.10-slim-bullseye
LABEL org.opencontainers.image.source https://github.com/sloppycoder/biznext_event_tool
LABEL org.opencontainers.image.description "BizNext event tool"

COPY . .

RUN pip install -r requirements.txt

USER 3001:3001
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000
