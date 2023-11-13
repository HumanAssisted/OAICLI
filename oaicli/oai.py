from . import OPEN_AI_MODEL_TYPE, DEFAULT_IMAGE_MODEL, threads_dir
from openai import OpenAI
import os
import logging
import click
import time
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
    # seems theres no api call to list threads? can't be named?
    for first_level in os.walk(threads_dir):
        thread_dir = first_level[1]
        break
    return [thread.split(thread_separator) for thread in thread_dir]


def create_thread(thread_name: str):
    empty_thread = client.beta.threads.create()
    thread_id = empty_thread.id
    click.echo(f"created thread {thread_id}.")
    os.makedirs(
        f"{threads_dir}/{thread_name}{thread_separator}{thread_id}", exist_ok=True
    )
    return (thread_name, thread_id)


def create_message(message_content: str, thread_name: str, thread_id: str):
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message_content,
    )
    # TODO save content locally in thread directory
    return thread_message


def create_run(thread_id, assistant_id):
    return client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )


def get_messages(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data


def wait_for_or_cancel_run(thread_id, run_id):
    timeout_is_ok = True
    total_time = 0
    MAX_TIME = 46
    CHECK_INCREMENT = 2
    click.echo(f"Running for a max of {MAX_TIME} seconds.")
    while timeout_is_ok:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status != "completed":
            click.echo(f"\r Job is {run.status}. {total_time} s passed.")
            time.sleep(CHECK_INCREMENT)
            total_time += CHECK_INCREMENT
            if run.status in ["cancelled", "failed", "expired"]:
                return
            if total_time >= MAX_TIME:
                run = client.beta.threads.runs.cancel(
                    thread_id="thread_abc123", run_id="run_abc123"
                )
        elif run.status == "completed":
            return True


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
