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
)
from . import ASCII_ART


@click.group()
def cli():
    click.echo(ASCII_ART)
    """Main entry point for oaicli."""
    pass


@click.group()
def agent():
    """Subcommand for managing agents."""
    pass


cli.add_command(agent)


@cli.command(name="start")
def start_up():
    """Get Started"""
    assistants = []
    current_assistant = None
    current_assistant_id = None
    threads = []
    current_thread = None
    current_thread_id = None
    current_run = None
    current_run_id = None

    click.echo("Listing assistants...")
    assistant_count = 0
    for assistant in get_assistants():
        assistants.append(assistant)
        click.echo(f"{assistant_count}. - {assistant.id} ({assistant.name})")
        assistant_count += 1

    if len(assistants) == 0:
        click.echo("No assistants not found.")
    else:
        assistant_choice = int(click.prompt("Select Assistant"))
        current_assistant = assistants[assistant_choice]
        current_assistant_id = current_assistant.id

    if click.confirm("Create new assistant?"):
        name = click.prompt("Name")
        input_type = click.prompt("File or enter instructions manually?", default="m")
        if input_type == "m":
            instructions = click.prompt("Instructions")
        else:
            click.echo("Filepath not supported yet")

        new_assistant = create_assistant_wrapper(name=name, instructions=instructions)
        click.echo(f"created {new_assistant.id} ({new_assistant.name})")
        assistants.append(new_assistant)
        current_assistant = new_assistant
        current_assistant_id = new_assistant.id

    # get threads
    # click.echo("Listing threads...")

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
    try:
        current_thread = threads[thread_choice]
        current_thread_id = current_thread[1]
        thread_name = current_thread[0]
    except Exception as e:
        exit(e)
    # create thread (add name to metadata)

    # thread loop
    click.echo("Ready. Type 'exit' when done.")
    while True:
        user_query = click.prompt(f"oaicli ({thread_name}) >")
        if user_query == "exit":
            exit("bye")

        # add message to thread
        thread_message = create_message(
            message_content=user_query,
            thread_name=current_thread[1],
            thread_id=current_thread_id,
        )
        click.echo(f"sent message {thread_message.id}")
        # ask if more messages (recurse)

        # run job
        current_run = create_run(current_thread_id, current_assistant_id)
        current_run_id = current_run.id

        # wait for result
        result = wait_for_or_cancel_run(current_thread_id, current_run_id)
        if not result:
            continue

        # when complete get thread/messages
        thread_messages = get_messages(current_thread_id)
        for content in thread_messages[0].content:
            click.echo(content.text.value)

        # [ThreadMessage(
        #     id='msg_n53ZT0m8pQZSbLhTPlBeNdJw',
        #     assistant_id='asst_xz5Kmdsk1Hs8t2ZLUWGRwnF2',
        #     content=[MessageContentText(text=Text(annotations=[],
        #         value='Hello! How can I assist you today?'),
        #         type='text')],
        #     created_at=1699873243, file_ids=[], metadata={}, object='thread.message', role='assistant',
        #     run_id='run_wediOA6p2gqQfFxsFnA2XvXZ', thread_id='thread_TkTvmaEJ3Pc0FcWS1Qo16QVD'),
        # ThreadMessage(id='msg_1s4T6hIVBQPOmmOo4zGyoIpR', assistant_id=None,
        #     content=[MessageContentText(text=Text(annotations=[], value='hello'), type='text')],
        #     created_at=1699873242, file_ids=[], metadata={}, object='thread.message', role='user',
        #     run_id=None, thread_id='thread_TkTvmaEJ3Pc0FcWS1Qo16QVD')
        # ]


@agent.command(name="list")
def list_agents():
    """List agents."""
    click.echo("Listing agents...")


@agent.command(name="create")
@click.argument("agent_name")
def create_agent(agent_name):
    """Create a new agent."""
    click.echo(f"Creating agent: {agent_name}")
    input_type = click.prompt("File or enter instructions manually?", default="m")
    if input_type == "m":
        instructions = click.prompt("Instructions:", default=42.0)
    # todo chose tools


@agent.command(name="edit")
@click.argument("agent")
@click.argument("field", type=click.Choice(["prompt", "name", "params"]))
def edit_agent(agent, field):
    """Edit something about the agent."""
    click.echo(f"Editing {field} of agent {agent}")


@agent.command(name="delete")
@click.argument("agent")
def delete_agent(agent):
    """Delete an agent."""
    click.echo(f"Deleting agent: {agent}")


@agent.command(name="file-upload")
@click.argument("agent")
@click.argument("path")
def file_upload(agent, path):
    """Send a file to your agent."""
    # creates a file

    # get agent

    # update agent

    # adds file to agent
    click.echo(f"Uploading file from {path} to agent {agent}")


@agent.command(name="directory-upload")
@click.argument("agent")
@click.argument("path")
def directory_upload(agent, path):
    """Uploads all text and PDF files from a directory."""
    click.echo(f"Uploading files from directory {path} to agent {agent}")


@agent.command(name="url-upload")
@click.argument("agent")
@click.argument("url")
def url_upload(agent, url):
    """Upload content from a URL to an agent."""
    click.echo(f"Uploading content from {url} to agent {agent}")


@agent.command(name="file-list")
@click.argument("agent")
def file_list(agent):
    """List an agent's files."""
    click.echo(f"Listing files for agent {agent}")


@click.group()
def thread():
    """Subcommand for managing threads."""
    pass


cli.add_command(thread)


# @thread.command(name="list")
# @click.argument("agent")
# def list_threads(agent):
#     """List current threads for an agent."""
#     click.echo(f"Listing threads for agent {agent}")


# @thread.command(name="join")
# @click.argument("agent")
# @click.argument("thread_choice")
# def join_thread(agent, thread_choice):
#     """Join a thread."""
#     click.echo(f"Joining thread {thread_choice} for agent {agent}")


@thread.command(name="new")
@click.argument("agent")
@click.argument("thread_title")
def new_thread(agent, thread_title):
    """Create a new thread."""
    click.echo(f"Creating new thread '{thread_title}' for agent {agent}")


def main():
    cli()


if __name__ == "__main__":
    main()
