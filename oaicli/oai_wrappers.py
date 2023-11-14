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
    _get_assistant_path,
    load_instructions,
    save_instructions,
    client,
)
from . import FilePathType


def create_agent_interactive():
    name = click.prompt("Name")
    input_type = click.prompt(
        "Load an instructions file or enter instructions manually?",
        type=click.Choice(["f", "m"]),
        default="m",
    )
    if input_type == "m":
        instructions = click.prompt("Instructions")
    else:
        file_path = click.prompt("Please enter a file path", type=FilePathType())
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
    click.echo(f"current instructions are {current_assistant.instructions}")
    if click.confirm(f"Update prompt?"):
        filepath = f"{_get_assistant_path(current_assistant)}/instructions.txt"
        if click.confirm(f"did you update {filepath}?"):
            new_instructions = None
        else:
            new_instructions = click.prompt("enter new instructions")
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
        file_path = file_path = click.prompt(
            "Please enter a file path", type=FilePathType()
        )
        if click.confirm(f"Are you sure you want to upload {file_path}?"):
            file = upload_file(file_path)
            file_id = file.id
    else:
        file_id = select_file_id()
    return file_id


def update_agent_with_file(assistant_id):
    # get agent
    my_assistant = client.beta.assistants.retrieve(assistant_id)

    my_assistant.file_ids += choose_or_create_file()
    # update agent
    client.beta.assistants.update(
        my_assistant.id,
        instructions=my_assistant.instructions,
        name=my_assistant.name,
        tools=my_assistant.tools,
        model=my_assistant.modal,
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

    click.echo(f"current instructions:\n {my_assistant.instructions}")

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
            model=my_assistant.modal,
            file_ids=my_assistant.file_ids,
        )


def update_agent_tools(assistant_id, tools_to_add=None, tools_to_remove=None):
    pass


def select_file_id():
    all_files = list_files()
    if len(all_files) > 0:
        choices = [
            (file.filename, file.id)
            for file in all_files
            if file.purpose == "assistants"
        ]
        indexes = []
        for index, (filename, fileid) in choices:
            indexes.append(0)
            click.echo(f"{index}. {filename}")

        index_choice = click.prompt("Choose a file index", type=click.Choice(indexes))

        file_choice = choices[index_choice]
        click.echo(f"You chose file {file_choice[0]} ({file_choice[1]})")
        return file_choice[1]


def list_assistants():
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
