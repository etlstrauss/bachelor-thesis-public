# based on https://github.com/open-webui/pipelines/blob/main/examples/pipelines/providers/openai_dalle_manifold_pipeline.py
"""A manifold to integrate OpenAI's ImageGen models into Open-WebUI"""

from typing import List, Union, Generator, Iterator

from pydantic import BaseModel

from openai import OpenAI

class Pipeline:
    """OpenAI ImageGen pipeline"""


    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "python_code_pipeline"
        self.name = "Image Usage Pipeline"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")


        message = ""
        message += "![image](" + <url> + ")\n"

        yield message