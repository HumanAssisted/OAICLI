import click
from .oai import (
    # ALL_TOOLS_AVAILABLE,
    create_assistant_wrapper,
    get_assistants,
    list_threads,
    create_thread,
    create_message,
    download_all_files,
    create_run,
    wait_for_or_cancel_run,
    get_messages,
)
from .oai_wrappers import create_agent_interactive, list_agents
from . import ASCII_ART, FilePathType


@click.group()
def cli():
    click.echo(ASCII_ART)
    """Main entry point for oaicli."""
    pass


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

    if click.confirm("Create new assistant?"):
        new_assistant = create_agent_interactive()
        assistants.append(new_assistant)
        current_assistant = new_assistant
        current_assistant_id = new_assistant.id

    assistants = list_agents()
    if len(assistants) > 0:
        assistant_choice = int(click.prompt("Select Assistant"))
        current_assistant = assistants[assistant_choice]
        current_assistant_id = current_assistant.id
    else:
        exit("must create assistant")

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
    click.echo("Ready.")
    click.echo(
        """
 - Change angent by typing "change agent"
 - Add file to
 - Type 'exit' when done."""
    )
    while True:
        user_query = click.prompt(f"oaicli ({thread_name}) >")
        if user_query.strip() == "exit":
            exit("bye")
        if user_query.strip() == "add":
            exit("bye")

        if click.confirm("Add a file?"):
            if click.confirm("Create a file?"):
                pass
            # list files
            # choose a file

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


@click.group()
def file():
    """Subcommand for managing file."""
    pass


cli.add_command(file)


@file.command(name="download_all")
def download_all():
    """Download all files"""
    download_all_files()


@click.group()
def agent():
    """Subcommand for managing agents."""
    pass


cli.add_command(agent)


@agent.command(name="list")
def list_agents():
    """List agents."""
    click.echo("Listing agents...")


@agent.command(name="create")
def create_agent():
    """Create a new agent."""
    create_agent_interactive()


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


def main():
    cli(auto_envvar_prefix="OAICLI")


if __name__ == "__main__":
    main()
