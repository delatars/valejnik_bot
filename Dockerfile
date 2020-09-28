FROM            python:3.7-alpine as builder

COPY            ./requirements.txt /libs/
WORKDIR         /libs

RUN             apk update && apk add --virtual build-dependencies \
                build-base \
                gcc \
                wget \
                git

RUN             pip install -r requirements.txt -t /libs


FROM            python:3.7-alpine

COPY            --from=builder /libs/ /usr/local/lib/python3.7/site-packages/
COPY            ./ /app
WORKDIR         /app

ENTRYPOINT      ["python", "entrypoint.py"]
