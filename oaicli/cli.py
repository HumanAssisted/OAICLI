import click
from .oai import (
    ALL_TOOLS_AVAILABLE,
    create_assistant_wrapper,
    get_assistants,
    create_assistant_wrapper,
    list_threads,
    create_thread,
)
from . import ASCII_ART


@click.group()
def cli():
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
    click.echo(ASCII_ART)
    assistants = []

    threads = []
    current_thread = None
    current_thread_id = None
    jobs = []
    current_job = None

    click.echo("Listing assistants...")
    for assistant in get_assistants():
        click.echo(f" - {assistant.id} ({assistant.name})")
        assistants.append(assistant)

    if len(assistants) == 0:
        click.echo("No assistants not found.")

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

    # get threads
    # click.echo("Listing threads...")

    for thread in list_threads():
        threads.append(thread)

    if len(threads) == 0:
        click.echo("No current threads.")

    if click.confirm("Create new thread?"):
        thread_name = click.prompt("Thread name?")
        new_thread = create_thread(thread_name=thread_name)
        threads.add(new_thread)

    # choose thread to send message to
    for index, thread in threads:
        click.echo(f"{index}. ")

    thread_choice = click.prompt("Choose a thread.")
    try:
        current_thread = threads[thread_choice]
        current_thread_id = current_thread.id
    except Exception as e:
        exit(e)
    # create thread (add name to metadata)

    # thread loop
    while True:
        user_query = click.prompt("oaicli >")
        if user_query == "exit":
            exit("bye")

        # add message to thread

        # ask if more messages (recurse)

        # run job

        # wait for result

        # display result


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


@thread.command(name="list")
@click.argument("agent")
def list_threads(agent):
    """List current threads for an agent."""
    click.echo(f"Listing threads for agent {agent}")


@thread.command(name="join")
@click.argument("agent")
@click.argument("thread_choice")
def join_thread(agent, thread_choice):
    """Join a thread."""
    click.echo(f"Joining thread {thread_choice} for agent {agent}")


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
