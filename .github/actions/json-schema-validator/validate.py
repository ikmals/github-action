from jsonschema import Draft7Validator
import os

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_files = os.getenv('INPUT_JSON_FILES')
event = os.getenv('GITHUB_EVENT_PATH')

print(event)