# based on https://github.com/FlowiseAI/Flowise/discussions/2581#discussioncomment-10607580

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import json
import reana_commons.validation.utils as rcv
import yaml
import re

class Pipeline:
    class Valves(BaseModel):
        pass  # No API key needed for Flowise API

    def __init__(self):
        self.name = "Reana-RAG-Presentation"
        self.valves = self.Valves()

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")

        print(messages)
        print(user_message)

        API_URL = "http://141.33.165.24:8000/api/v1/prediction/6b74c5bd-bcf9-4a29-824f-06d0028cce74"

        headers = {
            "Content-Type": "application/json"
        }

        # Creating the payload based on your example
        payload = {
            "question": user_message
        }

        print("Payload:", payload)

        try:
            r = requests.post(
                url=API_URL,
                json=payload,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            if body.get("stream"):
                text = ""
                for line in r.iter_lines():
                    line_data = line.decode('utf-8')
                    print("Line data:", line_data)
                    # Parse the JSON line and extract the text part
                    response_json = json.loads(line_data)
                    if "text" in response_json:
                        print("Streaming text:", response_json["text"])
                        text += response_json["text"]
                validation = False
                try:
                    data = yaml.safe_load(re.split(r'```.*?\n', text)[1].split("```")[0])
                    if(len(rcv.validate_reana_yaml(data)) < 1):
                        validation = True
                except Exception as e:
                        print("Error:", e)
                        validation = False
                    
                if(validation):
                    return "# This yaml specifications should work. \n" + text
                else:
                    return "# The response is not a valid REANA YAML. Please generate again. \n" + text
            else:
                response_json = r.json()
                print("Response JSON:", response_json)
                # Return only the "text" part of the response
                if "text" in response_json:
                    print("Text:", response_json["text"])
                    validation = False
                    try:
                        data = yaml.safe_load(response_json["text"].split("```")[1].split("```")[0])
                        if(len(rcv.validate_reana_yaml(data)) < 1):
                            validation = True
                    except Exception as e:
                            print("Error:", e)
                            validation = False
                    
                    if(validation):
                        return response_json["text"]
                    else:
                        return "The response is not a valid REANA YAML. Please generate again."
                else:
                    print("No text in response")
                    return "No text in response"
        except Exception as e:
            print("Error:", e)
            return f"Error: {e}"
