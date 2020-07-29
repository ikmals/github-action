FROM python:3.7-slim-stretch

RUN pip install jsonschema requests

COPY entrypoint.sh /entrypoint.sh
COPY validate.py /validate.py

RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
