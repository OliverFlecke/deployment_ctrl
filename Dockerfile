FROM alpine:latest

RUN apk add git
RUN apk add python3 py3-pip

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENV LOG_LEVEL=INFO
ENV ROOT_DIR=
ENV MQTT_URL=

ENTRYPOINT [ "python3", "app.py" ]