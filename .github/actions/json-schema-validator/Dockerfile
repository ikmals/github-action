FROM python:3

RUN pip install jsonschema requests

COPY validate.py /
CMD [ "python", "./validate.py" ]