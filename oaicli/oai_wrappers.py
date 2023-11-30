import click
from .oai import (
    # ALL_TOOLS_AVAILABLE,
    create_assistant_wrapper,
    get_assistants,
    list_threads,
    create_thread,
    list_files,
    upload_file,
    save_local_message,
    create_run,
    wait_for_or_cancel_run,
    get_messages,
    load_instructions,
    save_instructions,
    client,
)

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import HTML


import textwrap
from datetime import datetime


session = PromptSession()


def mutliline_toolbar():
    return HTML("To save press ESC then enter.")


def wrap_text(text, width=150, dash=False):
    wrapper = textwrap.TextWrapper(
        width=width, break_long_words=False, replace_whitespace=False
    )
    wrapped_lines = wrapper.wrap(text)

    if dash:
        wrapped_lines = [
            line + "-" if i < len(wrapped_lines) - 1 else line
            for i, line in enumerate(wrapped_lines)
        ]
    return "\n".join(wrapped_lines)


def create_agent_interactive():
    name = click.prompt("Name")
    input_type = click.prompt(
        "Load an instructions file or enter instructions manually?",
        type=click.Choice(["f", "m"]),
        default="m",
    )
    if input_type == "m":
        # instructions = click.prompt("Instructions")
        instructions = session.prompt(
            "Instructions",
            multiline=True,
            mouse_support=True,
            bottom_toolbar=mutliline_toolbar,
        )
    else:
        completer = PathCompleter()
        file_path = session.prompt("Enter a file path: ", completer=completer)

        click.echo(f"Loading filepath {file_path}")
        with open(file_path, "r") as filehandle:
            instructions = filehandle.read()
    new_assistant = create_assistant_wrapper(name=name, instructions=instructions)
    save_instructions(new_assistant, new_assistant.instructions)
    click.echo(f"created {new_assistant.id} ({new_assistant.name})")
    return new_assistant


def select_assistant():
    assistants = list_assistants()
    current_assistant = None
    if len(assistants) > 0:
        assistant_choice = int(click.prompt("Select Assistant"))
        current_assistant = assistants[assistant_choice]
    else:
        exit("must create assistant")
    return current_assistant


def update_agent():
    """Update an agents instructions or file list"""
    assistant = select_assistant()
    current_assistant = assistant
    current_assistant_id = assistant.id
    formatted_instructions = current_assistant.instructions  # wrap_text()
    click.echo(f"current instructions:\n\n\t{formatted_instructions}\n")
    click.echo(f"current files:\n{current_assistant.file_ids}\n")
    if click.confirm(f"Update prompt?"):
        if click.confirm(f"did you update {current_assistant.id}/instructions.txt?"):
            new_instructions = None
        else:
            completer = PathCompleter()
            file_path = session.prompt("Enter a file path: ", completer=completer)

            click.echo(f"Loading filepath {file_path}")
            with open(file_path, "r") as filehandle:
                new_instructions = filehandle.read()
        update_agent_instructions(
            current_assistant_id, new_instructions=new_instructions
        )

    if click.confirm(f"Update agents files?"):
        # select file from list of files
        update_agent_with_file(current_assistant_id)


def select_thread():
    thread = None
    threads = list_threads()

    if threads and len(threads) == 0:
        click.echo("No current threads.")

    if click.confirm("Create new thread?"):
        thread_name = click.prompt("Thread name?")
        new_thread = create_thread(thread_name=thread_name)
        threads.append(new_thread)

    # choose thread to send message to
    for index, thread in enumerate(threads):
        click.echo(f"{index}. {thread[0]}")

    thread_choice = int(click.prompt("Choose a thread."))
    current_thread = threads[thread_choice]
    return current_thread


def choose_or_create_file():
    if click.confirm("Create new file?"):
        completer = PathCompleter()
        file_path = session.prompt("Enter a file path: ", completer=completer)

        if click.confirm(f"Are you sure you want to upload {file_path}?"):
            file = upload_file(file_path)
            file_id = file.id
    else:
        file_id = select_file_id()
    return file_id


def update_agent_with_file(assistant_id):
    # get agent
    my_assistant = client.beta.assistants.retrieve(assistant_id)
    chosen_file_id = choose_or_create_file()
    my_assistant.file_ids.append(chosen_file_id)
    # update agent
    client.beta.assistants.update(
        my_assistant.id,
        instructions=my_assistant.instructions,
        name=my_assistant.name,
        tools=my_assistant.tools,
        model=my_assistant.model,
        file_ids=my_assistant.file_ids,
    )


def run_thread(current_thread_id, current_assistant_id):
    # run job
    current_run = create_run(current_thread_id, current_assistant_id)
    current_run_id = current_run.id

    # wait for result
    result = wait_for_or_cancel_run(current_thread_id, current_run_id)
    if not result:
        return

    # when complete get thread/messages
    thread_messages = get_messages(current_thread_id)
    for content in thread_messages[0].content:
        save_local_message(thread_message=thread_messages[0], role="assistant")
        click.echo(content.text.value)


def update_agent_instructions(assistant_id, new_instructions=None):
    # get agent
    my_assistant = client.beta.assistants.retrieve(assistant_id)

    if new_instructions:
        # save them
        save_instructions(my_assistant, new_instructions)
    else:
        # they are updated locally
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
            model=my_assistant.model,
            file_ids=my_assistant.file_ids,
        )


def update_agent_tools(assistant_id, tools_to_add=None, tools_to_remove=None):
    pass


def select_file_id():
    all_files = list_files()
    choices = [
        (file.filename, file.id, file.created_at)
        for file in all_files
        if file.purpose == "assistants"
    ]
    indexes = []
    for index, (filename, fileid, created) in enumerate(choices):
        indexes.append(str(index))
        dt = datetime.fromtimestamp(created)
        created = dt.strftime("%Y-%m-%d-%H:%M:%S")
        click.echo(f"{index}. {filename} ({created})")

    index_choice = click.prompt("Choose a file index", type=click.Choice(indexes))

    file_choice = choices[int(index_choice)]
    click.echo(f"You chose file {file_choice[0]} ({file_choice[1]})")
    return file_choice[1]


def list_assistants():
    assistants = []
    click.echo("Listing assistants...")
    assistant_count = 0
    for assistant in get_assistants():
        assistants.append(assistant)
        click.echo(f"{assistant_count}. {assistant.name}({assistant.id})")
        assistant_count += 1

    if len(assistants) == 0:
        click.echo("No assistants not found.")
    return assistants
