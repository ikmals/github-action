FROM python:3

RUN apk add --no-cache \
    jq

RUN pip install jsonschema requests

COPY entrypoint.sh /entrypoint.sh
COPY validate.py /validate.py

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]