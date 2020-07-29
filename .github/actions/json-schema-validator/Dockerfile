FROM python:3

RUN pip install jsonschema requests

COPY . .
CMD [ "python", "./validate.py" ]