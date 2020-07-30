import json
import os
import re

import requests
from jsonschema import Draft7Validator

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_path_pattern = os.getenv('INPUT_JSON_PATH_PATTERN')
send_comment = os.getenv('INPUT_SEND_COMMENT')
clear_comments = os.getenv('INPUT_CLEAR_COMMENTS')
token = os.getenv('INPUT_TOKEN')

event_path = os.getenv('GITHUB_EVENT_PATH')


def query(headers, url, data=None):
    if data is not None:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)
        # print('headers')
        # print(headers)
        # response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Status code {}: {}'.format(response.status_code, url))


def validate_file(json_schema, json_path_pattern, file_path):
    pattern = re.compile(json_path_pattern)
    if pattern.match(file_path):
        print('validating')
        schema = json_from_file(json_schema)
        validator = Draft7Validator(schema)
        for error in sorted(validator.iter_errors(instance), key=str):
            validation_error = {}
            validation_error['message'] = error.message
            validation_error['validator'] = error.validator
            validation_error['validator_value'] = error.validator_value

            validation_errors.append(validation_error)

        return validation_errors
    else:
        print('{} doesn\'t match pattern {}'.format(file_path, json_path_pattern))
        return []


def clear_comments():
    return True


def send_comment(errors):
    return True


def json_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


event = json_from_file(event_path)
changed_files_url = event['pull_request']['_links']['self']['href'] + '/files'
headers = {"Authorization": "Bearer {}".format(token)}

errors = []
changed_files = query(headers, changed_files_url)
for changed_file in changed_files:
    filename = changed_file['filename']
    validation_errors = validate_file(json_schema, json_path_pattern, filename)

    if len(validation_errors):
        errors.append(validation_errors)

if len(errors):
    if send_comment:
        send_comment(errors)

    for error in errors:
        print(error)
