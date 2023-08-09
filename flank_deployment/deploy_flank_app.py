import json
import requests
import os

def lambda_handler(event, context):
    if "env_ref" in event:
        env_ref = event["env_ref"]
    else:
        env_ref = "fomf"
    
    # TODO implement
    headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {os.getenv("flank_github_token")}',
    'X-GitHub-Api-Version': '2022-11-28',
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = '{"ref":"develop","inputs":{}}'
    
    file_name = get_workflow_file_name(env_ref)
    
    response = requests.post(
        f'https://api.github.com/repos/btf-org/flank-app/actions/workflows//dispatches',
        headers=headers,
        data=data,
    )
    
    print("resp ", response)
    
    if response.status_code >= 200 and response.status_code < 300:
        return "Kicked off the workflow successfully"
    
    return "There was an error kicking off the workflow"

def get_workflow_file_name(env_ref):
    if env_ref == "aws-dev":
        return "aws-deploy-dev.yml"
    elif env_ref == "aws-prod":
        return "aws-deploy-prod.yml"
    elif env_ref == "comc":
        return "comc-deploy-prod.yml"
    else:
        return "fomf-deploy-dev.yml"