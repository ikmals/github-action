#!/bin/bash

jq --raw-output . "$GITHUB_EVENT_PATH"
python /validate.py