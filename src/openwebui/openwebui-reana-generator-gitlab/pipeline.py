# source: https://github.com/FlowiseAI/Flowise/discussions/2581#discussioncomment-10607580

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import json

class Pipeline:
    class Valves(BaseModel):
        pass  # No API key needed for Flowise API

    def __init__(self):
        self.name = "Reana-To-Gitlab"
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

        API_URL = "http://141.33.165.24:8000/api/v1/prediction/2481e3f0-8f6d-440a-b0d0-133ed1c02356"

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
                for line in r.iter_lines():
                    line_data = line.decode('utf-8')
                    print("Line data:", line_data)
                    # Parse the JSON line and extract the text part
                    response_json = json.loads(line_data)
                    if "text" in response_json:
                        print("Streaming text:", response_json["text"])
                        yield response_json["text"]
            else:
                response_json = r.json()
                print("Response JSON:", response_json)
                # Return only the "text" part of the response
                if "text" in response_json:
                    print("Text:", response_json["text"])
                    return response_json["text"]
                else:
                    print("No text in response")
                    return "No text in response"
        except Exception as e:
            print("Error:", e)
            return f"Error: {e}"