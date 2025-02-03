import requests
from langchain_community.document_loaders import GitLoader
import io

# pushes vecotrized data to FlowiseAI conencted to Qdrant
def pushToFlowise(file_like_object, file_name):
    API_URL =  "http://141.33.165.24:8000/api/v1/vector/upsert/ac04a85d-3a13-409c-b4eb-dcd40b9ef742"
    # use form data to upload files
    form_data = {
        "files": (file_name, file_like_object)
    }
    body_data = {
    }

    def query(form_data, body_data):
        response = requests.post(API_URL, files=form_data, data=body_data)
        return response.json()

    query(form_data, body_data)


# load yaml files from git repo
loader = GitLoader(repo_path="/home/tom/Documents/HOST/Bachelorarbeit/reana-tutorials-github")
data = loader.load()
for i in range(len(data)):
    file_data = data[i].metadata.get('source').split('/')
    if('.yaml' in file_data[len(file_data)-1]):
        file_like_object = io.StringIO(data[i].page_content)
        file_name = ""
        for j in range(len(file_data)-1):
            file_name += file_data[j] + '-'
        pushToFlowise(file_like_object, file_name)
        print("Pushed: " + data[i].metadata.get('source'))