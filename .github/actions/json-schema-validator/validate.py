import json
import os
import re

import jq
import requests
from jsonschema import Draft7Validator

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_path_pattern = os.getenv('INPUT_JSON_PATH_PATTERN')
send_comment = os.getenv('INPUT_SEND_COMMENT')
clear_comments = os.getenv('INPUT_CLEAR_COMMENTS')

event_path = os.getenv('GITHUB_EVENT_PATH')
repo = os.getenv('GITHUB_REPOSITORY')


def query(url, data=None):
    headers = {'Authorization': 'Bearer {}'.format(os.getenv('INPUT_TOKEN'))}

    if data is not None:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Status code {}: {}'.format(response.status_code, url))


def validate_file(json_schema, json_path_pattern, file_path):
    pattern = re.compile(json_path_pattern)
    if pattern.match(file_path):
        print('validating {}'.format(file_path))
        schema = json_from_file(json_schema)
        instance = json_from_file(file_path)

        validator = Draft7Validator(schema)
        for error in sorted(validator.iter_errors(instance), key=str):
            validation_error = {}
            validation_error['path'] = file_path
            validation_error['message'] = error.message
            validation_error['validator'] = error.validator
            validation_error['validator_value'] = error.validator_value

            validation_errors.append(validation_error)

        return validation_errors
    else:
        print('{} doesn\'t match pattern {}'.format(
            file_path, json_path_pattern))
        return []


def clear_comments():
    return True


def send_comment(errors):
    formatted_errors = []
    for error in errors:
        path = error['path']
        message = error['message']
        validator = error['validator']
        validator_value = error['validator_value']

        formatted = MESSAGE.format(
            path=path, message=message, validator=validator, validator_value=validator_value)
        formatted_errors.append(formatted)

    joined_errors = '\r\n\r\n'.join(formatted_errors)
    
    comment_url = ISSUE_COMMENTS.format(repo=repo, issue_number=pull_number)
    body = {'body': joined_errors}
    res = query(comment_url, body)
    print(res)


def json_from_file(file_path):
    with open(file_path) as f:
        return json.load(f)


BASE = 'https://api.github.com'
PR_FILES = BASE + '/repos/{repo}/pulls/{pull_number}/files'
ISSUE_COMMENTS = BASE + '/repos/{repo}/issues/{issue_number}/comments'
MESSAGE = '''**JSON Schema validation failed for `{path}`.**
            **Message** : `{message}`
            **Validator** : `{validator}`
            **Validator Rule** : `{validator_value}`'''

event = json_from_file(event_path)
pull_number = jq.compile('.pull_request.number').input(event).first()


errors = []
pr_files_url = PR_FILES.format(repo=repo, pull_number=pull_number)
pr_files = query(pr_files_url)

for pr_file in pr_files:
    filename = pr_file['filename']
    validation_errors = validate_file(json_schema, json_path_pattern, filename)

    if len(validation_errors):
        errors.append(validation_errors)

if len(errors):
    if send_comment:
        send_comment(errors)

    for error in errors:
        print(error)

    # raise Exception('Fail validation')
