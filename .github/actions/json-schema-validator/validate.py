from jsonschema import Draft7Validator
import requests
import os
import json

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_path_pattern = os.getenv('INPUT_JSON_PATH_PATTERN')
send_comment = os.getenv('INPUT_SEND_COMMENT')
clear_comments = os.getenv('INPUT_CLEAR_COMMENTS')

event_path = os.getenv('GITHUB_EVENT_PATH')
token = os.getenv('GITHUB_TOKEN')


def query(headers, url, data=None):
    if data is not None:
        response = requests.post(url, json=data, headers=headers)
    else:
        response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Status code {}: {}'.format(response.status_code, url))


def validate_file(json_schema, json_path_pattern, file_path):
    return []


def clear_comments():
    return True


def send_comment(errors):
    return True


with open(event_path) as f:
    event = json.load(f)

changed_files_url = event['pull_request']['_links']['self']['href'] + '/files'
headers = {"Authorization": "token {}".format(token)}

errors = []
changed_files = query(headers, changed_files_url)
for changed_file in changed_files:
    filename = changed_file['filename']
    validation_errors = validate_file(json_schema, json_path_pattern, filename)

    if len(validation_errors):
        errors.append(validation_errors)

if len(errors):
    if send_comment:
        create_comment(errors)

    for error in errors:
        print(error)
