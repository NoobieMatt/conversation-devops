import json
import requests
import base64

# env variables
prod_workspace_id = '' # only fill in if you already have a prod workspace
prod_username = '' # conversation prod username
prod_password = '' # conversation prod password
github_username = ''
github_access_token = '' # personal access token for auth
repo = ''
github_endpoint = 'https://api.github.com/repos/%s/%s/contents/workspace.json' % (github_username, repo)
conversation_url = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces?version=2017-05-26'
update_conversation_url = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces/%s?version=2017-05-26' % (prod_workspace_id)

# get json from github
def get_file():
    # get workspace json
    data = requests.get(github_endpoint, auth=(github_username, github_access_token)).json()
    # decode data
    data = base64.b64decode(data['content'])
    data = json.loads(data)

    return data

workspace = get_file()

# create new workspace in prod instance
def create_workspace(workspace):
    response = requests.post(conversation_url, auth=(prod_username, prod_password), json=workspace)
    print response

# update production workspace
def update_workspace(workspace):
    response = requests.post(update_conversation_url, auth=(prod_username, prod_password), json=workspace)
    print response

# run create or update
create_workspace(workspace)
# update_workspace(workspace)
