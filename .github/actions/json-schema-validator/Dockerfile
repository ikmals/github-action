# FROM python:3

# RUN apk add --update --no-cache curl jq

# RUN pip install jsonschema requests

# COPY entrypoint.sh /entrypoint.sh
# COPY validate.py /validate.py

# RUN chmod +x /entrypoint.sh
# ENTRYPOINT [ "/entrypoint.sh" ]

FROM stedolan/jq
CMD ["jq", "--raw-output", ".", '"$GITHUB_EVENT_PATH"']