import click
from .oai import (
    # ALL_TOOLS_AVAILABLE,
    create_assistant_wrapper,
    get_assistants,
    list_threads,
    create_thread,
    create_message,
    create_run,
    wait_for_or_cancel_run,
    get_messages,
    _get_assistant_path,
    load_instructions,
    save_instructions,
    client,
)
from . import ASCII_ART, FilePathType


def create_agent_interactive():
    name = click.prompt("Name")
    input_type = click.prompt(
        "Load file or enter instructions manually?",
        type=click.Choice(["f", "m"]),
        case_sensitive=False,
        default="m",
    )
    if input_type == "m":
        instructions = click.prompt("Instructions")

    else:
        file_path = click.prompt("Please enter a file path", type=FilePathType())
        click.echo(f"Loading filepath {file_path}")
    new_assistant = create_assistant_wrapper(name=name, instructions=instructions)
    save_instructions(new_assistant, new_assistant.instructions)
    click.echo(f"created {new_assistant.id} ({new_assistant.name})")
    return new_assistant


def update_agent_with_file(assistant_id, file_path):
    # get agent
    my_assistant = client.beta.assistants.retrieve(assistant_id)

    # list files current agent files

    # get list of local files

    # choose file to update

    # add file id to list

    # update agent
    pass


def update_agent_instructions(assistant_id, new_instructions=None):
    # get agent
    my_assistant = client.beta.assistants.retrieve(assistant_id)

    click.echo(f"current instructions:\n {my_assistant.instructions}")

    if new_instructions:
        save_instructions(my_assistant, new_instructions)
    else:
        new_instructions = load_instructions(my_assistant)

    if click.confirm(f"new instructions OK? \n{new_instructions}"):
        # change instructions
        my_assistant.instructions = new_instructions
        # update agent
        client.beta.assistants.update(
            my_assistant.id,
            instructions=my_assistant.instructions,
            name=my_assistant.name,
            tools=my_assistant.tools,
            model=my_assistant.modal,
            file_ids=my_assistant.file_ids,
        )


def update_agent_tools(assistant_id, tools_to_add=None, tools_to_remove=None):
    pass


def select_file_id():
    pass


def list_agents():
    assistants = []
    click.echo("Listing assistants...")
    assistant_count = 0
    for assistant in get_assistants():
        assistants.append(assistant)
        click.echo(f"{assistant_count}. - {assistant.id} ({assistant.name})")
        assistant_count += 1

    if len(assistants) == 0:
        click.echo("No assistants not found.")
    return assistants


def add_file_to_agent():
    # https://platform.openai.com/docs/api-reference/assistants/createAssistantFile
    file_path = _get_assistant_path()
    pass


def add_file_to_message():
    pass
