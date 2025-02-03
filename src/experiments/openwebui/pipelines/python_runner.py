# this code is based on a example from the openwebui pipline repository (https://github.com/open-webui/pipelines/blob/main/examples/pipelines/integrations/python_code_pipeline.py)

from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
import subprocess
import requests

class Pipeline:
    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "python_code_pipeline"
        self.name = "Python Code Pipeline"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def execute_python_code(self, code):
        try:
            result = subprocess.run(
                ["python", "-c", code], capture_output=True, text=True, check=True
            )
            stdout = result.stdout.strip()
            return stdout, result.returncode
        except subprocess.CalledProcessError as e:
            return e.output.strip(), e.returncode

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        print(messages)
        print(user_message)


        url = 'http://141.33.165.24:8000/api/v1/prediction/5467f902-a69f-4bb1-8db7-40a70da88d64'

        headers = {'Content-Type': 'application/json'}
        data = {'question': user_message}

        response = requests.post(url,  json=data, headers=headers) 
        if body.get("title", False):
            print("Title Generation")
            return "Python Code Pipeline"
        else:
            stdout, return_code = self.execute_python_code(response.json()['text'].split('```python')[1].split('```')[0])
            output = response.json()['text'] + '\n script output:\n' + stdout
            return output
