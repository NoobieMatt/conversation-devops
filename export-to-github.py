import json
import requests
import base64

# env variables
dev_workspace_id = '' # conversation workspace id
dev_username = '' # conversation dev username
dev_password = '' # conversation dev password
github_username = ''
github_access_token = '' # personal access token for auth
repo = ''
github_sha = ''
github_endpoint = 'https://api.github.com/repos/%s/%s/contents/workspace.json' % (github_username, repo)
conversation_url = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces/' + dev_workspace_id + '?version=2017-05-26'

# get workspace
data = requests.get(conversation_url,auth=(dev_username,dev_password),params={'export': 'true'}).json()
data = json.dumps(data)

# encode workspace data
data = base64.b64encode(data)

# CREATE NEW -------- for first time deployment
def create_file():
    payload = {
        "message": "create first copy of workspace",
        "content": data,
        "committer": { # committer is optional
            "name": "",
            "email": ""
        }
        # can add branch as optional
    }
    response = requests.put(github_endpoint, data=json.dumps(payload), auth=(github_username, github_access_token))
    print response.text
    return response

# UPDATE WORKSPACE --------
def update_file():
    # get file sha
    current_file = requests.get(github_endpoint, auth=(github_username, github_access_token)).json()
    github_sha = current_file['sha']

    # update file
    payload = {
        "message": "update workspace",
        "content": data,
        "committer": { # committer is optional
            "name": "",
            "email": ""
        },
        "sha": github_sha
    }
    response = requests.put(github_endpoint, data=json.dumps(payload), auth=(github_username, github_access_token))
    print response.text
    return response

# Run create or update
response = create_file()
# response = update_file()
