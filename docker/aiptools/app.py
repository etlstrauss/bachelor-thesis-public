# used chatgpt + copilot for brainstorming
# sources:
# https://www.devdungeon.com/content/working-git-repositories-python 
# https://gitpython.readthedocs.io/en/stable/tutorial.html#handling-remotes
# https://gitpython.readthedocs.io/en/stable/reference.html?highlight=push#git.remote.Remote.push
# https://stackoverflow.com/questions/10054318/how-do-i-provide-a-username-and-password-when-running-git-clone-gitremote-git
# https://stackoverflow.com/questions/1210458/how-can-i-generate-a-unique-id-in-python

from flask import Flask, request, jsonify
from reana_commons.validation import utils as rcv
import reana_client.api.client as rcl
import yaml
import re
import git
import os
import uuid
import credentails

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def sum():
    data = request.get_json()
    a = data.get('a')
    b = data.get('b')
    return jsonify({'sum': a + b})

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.get_json()
        reana_file = data.get('reana_file')
        print(len(rcv.validate_reana_yaml(yaml.safe_load(reana_file))))
        if(len(rcv.validate_reana_yaml(yaml.safe_load(reana_file)))<1):
            return jsonify({'validation': True})
        else:
            return jsonify({'validation': False})
    except Exception as e:
        return jsonify({'validation': False})
    
@app.route('/create_workflow', methods=['POST'])
def create_workflow():
    try:
        data = request.get_json()
        reana_file = data.get('reana_file')
        workflow_name = data.get('workflow_name')
        rcl.create_workflow(yaml.safe_load(reana_file), workflow_name, credentails.reana_api_key)
        return jsonify({'status': True})
    except Exception as e:
        return jsonify({'status': False})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()
        workflow_name = data.get('workflow_name')
        file_content = data.get('file_content')
        file_name = data.get('file_name')
        rcl.upload_file(workflow_name, file_content, file_name, credentails.reana_api_key)
        return jsonify({'status': True})
    except Exception as e:
        return jsonify({'status': False})
    
@app.route('/start_workflow', methods=['POST'])
def start_workflow():
    try:
        data = request.get_json()
        workflow_name = data.get('workflow_name')
        rcl.start_workflow(workflow_name, credentails.reana_api_key, None)
        return jsonify({'status': True})
    except Exception as e:
        return jsonify({'status': False})
    
@app.route('/full_upload', methods=['POST'])
def full_upload():
   try:
        random_id = "llm-gen-" + str(uuid.uuid4())
        data = request.get_json()
        files = re.split(r'```.*?\n', data.get('content'))
        files[len(files)-1] = files[len(files)-1].replace('```', '')
        files = list(filter(lambda item: item not in ['\n', ''], files))
        reana_file = yaml.safe_load(files[0])
        rcl.create_workflow(reana_file, random_id, credentails.reana_api_key)
        file_list = reana_file["inputs"]["files"]
        for i in range(1, len(files)):
            rcl.upload_file(random_id, files[i], file_list[i-1], credentails.reana_api_key)
        rcl.start_workflow(random_id, credentails.reana_api_key, None)
        return jsonify({'status': True, 'worflow_id': random_id})
   except Exception as e:
    return jsonify({'status': False})

@app.route('/push_to_gitlab', methods=['POST'])
def push_to_gitlab():
    try:
        def initialize_local_repo(repo_path, remote_url, token):
            if not os.path.exists(repo_path):
                os.makedirs(repo_path)
            
            repo = git.Repo.init(repo_path)
            print(f"Initialized a new git repository at {repo_path}")


            data = request.get_json()
            files = re.split(r'```.*?\n', data.get('content'))
            files[len(files)-1] = files[len(files)-1].replace('```', '')
            files = list(filter(lambda item: item not in ['\n', ''], files))
            reana_file = str(files[0])
            with open(f'{repo_path}reana.yaml', "w") as f:
                    f.write(reana_file)
            repo.index.add([f'{repo_path}reana.yaml'])
            file_list = yaml.safe_load(reana_file)["inputs"]["files"]
            for i in range(1, len(files)):
                with open(f'{repo_path}{file_list[i-1]}', "w") as f:
                    f.write(str(files[i]))
                repo.index.add([f'{repo_path}{file_list[i-1]}'])
            
            repo.index.commit("Initial commit")
            print("Created initial commit")

            origin = repo.create_remote('origin', remote_url)
            print(f"Added remote: {remote_url}")
            origin.push(refspec="master")
            print("Pushed to remote repository")
            
            return jsonify({'status': True})


        data = request.get_json()
        repo_name = data.get('repo_name')

        random_id = str(uuid.uuid4())

        
        initialize_local_repo(f'/app/{random_id}/', f'https://{credentails.gitlab_user}:{credentails.gitlab_passwd}@gitlab.aip.de/{credentails.gitlab_user}/{random_id}.git', credentails.gitlab_token)
        return jsonify({'status': True, 'repo_url': f'https://gitlab.aip.de/{credentails.gitlab_user}/{random_id}'})
    except Exception as e:
        return jsonify({'status': False})
if __name__ == '__main__':
    app.run(host='0.0.0.0')