from jsonschema import Draft7Validator
import requests
import os
import json

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_files = os.getenv('INPUT_JSON_FILES')
event_path = os.getenv('GITHUB_EVENT_PATH')
token = os.getenv('GITHUB_TOKEN')


def query(headers, url, data):
    if data is not None:
        response = requests.post(url, data)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code + ':' + query)


with open(event_path) as f:
    event = json.load(f)

changed_files_url = event['pull_requests']['_links']['self']['href'] + '/files'
headers = {"Authorization": "token {}".format(token)}

changed_files = query(headers, changed_files_url)
print(changed_files)