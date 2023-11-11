from . import OPEN_AI_MODEL_TYPE, DEFAULT_IMAGE_MODEL, threads_dir
from openai import OpenAI
import os
import logging
import click
import json
from typing import Optional, List

JSON_RESPONSE_TYPE = {"type": "json_object"}
TEXT_RESPONSE_TYPE = {"type": "text"}
ALL_TOOLS_AVAILABLE = []
MAX_AGENT_LIST = 100
thread_separator = "---"

logger = logging.getLogger("oaicli")

client = OpenAI()


def get_assistants(after=None):
    assistants = client.beta.assistants.list(
        order="desc",
        limit=MAX_AGENT_LIST,
        after=after,
    )
    for assistant in assistants:
        yield assistant
    if assistants.has_more:
        click.echo(f"There are more, but we stop at {MAX_AGENT_LIST}")
        # for assistent in get_assistants(after=None):
        #     yield assistent


def create_assistant_wrapper(
    name: str, instructions: str, tools: Optional[List[str]] = None
):
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        # tools=tools,
        model=OPEN_AI_MODEL_TYPE,
    )

    return my_assistant


def list_threads():
    # seems theres no api call so we use local
    for thread in os.walk(threads_dir):
        yield thread.split(thread_separator)


def create_thread(thread_name: str):
    empty_thread = client.beta.threads.create()
    thread_id = empty_thread.id
    os.makedirs(
        f"{threads_dir}/{thread_name}{thread_separator}{thread_id}", exist_ok=True
    )
    return empty_thread


def vision_url(prompt: str, image_url: str):
    response = client.chat.completions.create(
        model=DEFAULT_IMAGE_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": "low",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response
