# source: https://github.com/FlowiseAI/Flowise/discussions/2581#discussioncomment-10607580

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import json

class Pipeline:

    def __init__(self):
        self.name = "Reana-Final"
        pass

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        
        API_URL = "http://141.33.165.24:8000/api/v1/prediction/bddddad9-3b09-44f1-af80-e6788a58d906"

        headers = {
            "Content-Type": "application/json"
        }

        if(len(messages) > 1):
            user_message = user_message + "\n History:\n" + messages[len(messages)-2].get("content")


        payload = {
            "question": user_message,
        }

        try:
            r = requests.post(
                url=API_URL,
                json=payload,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            if body.get("stream"):
                for line in r.iter_lines():
                    line_data = line.decode('utf-8')
                    response_json = json.loads(line_data)
                    if "text" in response_json:
                        yield response_json["text"]
            else:
                response_json = r.json()
                if "text" in response_json:
                    return response_json["text"]
                else:
                    return "No text in response"
        except Exception as e:
            print.error(f"An error occurred: {e}")
            yield """An error occurred while processing the request:
                                Please only send tasks matching the topic REANA.
                                Here is a list of possible tasks:
                                - generate an workflow
                                - modify the last workflow
                                - upload to GitLab
                                - upload to REANA
                                Example for these are:
                                - "Please create an REANA workflow which,..."
                                - "Please change the parameter environment to python3.9-slim"
                                - "Please upload this to GitLab"
                                - "Please upload this to REANA"
                                You probably send harmful data"""