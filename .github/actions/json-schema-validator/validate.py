import json
import os
from distutils.util import strtobool

import jq
from jsonschema import Draft7Validator

from .utils import *

json_schema = os.getenv('INPUT_JSON_SCHEMA')
json_path_pattern = os.getenv('INPUT_JSON_PATH_PATTERN')
send_comment = strtobool(os.getenv('INPUT_SEND_COMMENT'))
clear_comments = strtobool(os.getenv('INPUT_CLEAR_COMMENTS'))

event_path = os.getenv('GITHUB_EVENT_PATH')
repo = os.getenv('GITHUB_REPOSITORY')

BASE = 'https://api.github.com'
PR_FILES = BASE + '/repos/{repo}/pulls/{pull_number}/files'
ISSUE_COMMENTS = BASE + '/repos/{repo}/issues/{issue_number}/comments'
DELETE_ISSUE_COMMENTS = BASE + '/repos/{repo}/issues/comments/{comment_id}'

COMMENT_HEADER = '**JSON Schema validation failed for `{path}`**'
COMMENT = '''
---
**Validator:** `{validator}`
**Validator value:**
```
{validator_value}
```
**Message:**
```
{message}
```
**Instance:**
```
{instance}
```'''

event = json_from_file(event_path)
pull_number = jq.compile('.pull_request.number').input(event).first()

errors = []
pr_files_url = PR_FILES.format(repo=repo, pull_number=pull_number)
pr_files = request('get', pr_files_url)

for pr_file in pr_files:
    filename = pr_file['filename']
    validation_errors = validate_file(json_schema, json_path_pattern, filename)

    if len(validation_errors):
        errors.append({
            'path': filename,
            'errors': validation_errors
        })

if clear_comments:
    delete_comments(repo, pull_number)

if len(errors):
    if send_comment:
        create_comment(repo, pull_number, errors)

    for error in errors:
        print(error)

    # raise Exception('Fail validation')
