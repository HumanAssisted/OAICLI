import click
from .oai import (
    # ALL_TOOLS_AVAILABLE,
    create_message,
    download_all_files,
    list_all_files,
    upload_file,
    delete_file,
    delete_assistant,
)
from .oai_wrappers import (
    create_agent_interactive,
    list_assistants,
    select_assistant,
    select_thread,
    update_agent,
    choose_or_create_file,
    run_thread,
    select_file_id,
)
from . import ASCII_ART, FilePathParamType
from prompt_toolkit import prompt


@click.group()
def cli():
    """Main entry point for oaicli."""
    pass


@cli.command(name="start")
def start_up():
    """Get Started"""
    click.echo(ASCII_ART)
    assistants = []
    current_assistant = None
    current_assistant_id = None

    if click.confirm("Create new assistant?"):
        new_assistant = create_agent_interactive()
        assistants.append(new_assistant)
        current_assistant = new_assistant
        current_assistant_id = new_assistant.id
    else:
        assistant = select_assistant()
        current_assistant = assistant
        current_assistant_id = assistant.id

    current_thread = select_thread()
    current_thread_id = current_thread[1]
    current_thread_name = current_thread[0]

    # thread loop
    click.echo("Ready.")
    click.echo(
        """
Inline commands:
 - Change agent by typing "change" (changes which agent runs the thread)
 - Add file to agent (or change prompt) with "agent"
 - Type 'exit' when done."""
    )
    while True:
        # user_query = click.prompt(f"oaicli ({current_thread_name}) >")
        user_query = prompt(f"oaicli ({current_thread_name}) >")
        if user_query.strip() == "exit":
            exit("bye")
        elif user_query.strip() == "change":
            click.echo("changing agent")
            continue
        elif user_query.strip() == "agent":
            update_agent()

        if click.confirm("Add a file to the message?"):
            file_id = choose_or_create_file()
            thread_message = create_message(
                message_content=user_query,
                thread_name=current_thread[1],
                thread_id=current_thread_id,
                file_ids=[file_id],
            )
        else:
            # add message to thread
            thread_message = create_message(
                message_content=user_query,
                thread_name=current_thread[1],
                thread_id=current_thread_id,
            )

        click.echo(f"sent message {thread_message.id}")
        run_thread(current_thread_id, current_assistant_id)


@click.group()
def file():
    """Subcommand for managing file."""
    pass


cli.add_command(file)


@file.command(name="download-all")
def download_all():
    """Download all files"""
    download_all_files()


@file.command(name="list")
def list_all():
    """List all files"""
    list_all_files()


@file.command(name="upload")
@click.option(
    "-f", "--file-path", type=FilePathParamType(), help="Path to a file.", required=True
)
def do_upload_file(file_path):
    """Upload file"""
    if click.confirm(f"Are you sure you want to upload {file_path}?"):
        upload_file(file_path)


@file.command(name="delete")
def do_delete_file():
    """delete file"""
    file_id = select_file_id()
    if click.confirm(f"Are you sure you want to delete file {file_id}?"):
        delete_file(file_id)


# @file.command(name="list_all")
# def upload_directory():
#     """List all files"""
#     list_all_files()


@click.group()
def agent():
    """Subcommand for managing agents."""
    pass


cli.add_command(agent)


@agent.command(name="list")
def list_agents():
    """List agents."""
    list_assistants()


@agent.command(name="create")
def create_agent():
    """Create a new agent."""
    create_agent_interactive()


@agent.command(name="update")
def do_update_agent():
    """Update an agents instructions or file list"""
    update_agent()


@agent.command(name="delete")
def do_delete_agent():
    """delete an agent"""
    assistant = select_assistant()
    if click.confirm(
        f"Are you sure you want to delete assistant {assistant.name} ({assistant.id})?"
    ):
        delete_assistant(assistant.id)


# @agent.command(name="delete")
# @click.argument("agent")
# def delete_agent(agent):
#     """Delete an agent."""
#     click.echo(f"Deleting agent: {agent}")


# @agent.command(name="file-upload")
# @click.argument("agent")
# @click.argument("path")
# def file_upload(agent, path):
#     """Send a file to your agent."""
#     # creates a file

#     # get agent

#     # update agent

#     # adds file to agent
#     click.echo(f"Uploading file from {path} to agent {agent}")


# @agent.command(name="directory-upload")
# @click.argument("agent")
# @click.argument("path")
# def directory_upload(agent, path):
#     """Uploads all text and PDF files from a directory."""
#     click.echo(f"Uploading files from directory {path} to agent {agent}")


# @agent.command(name="url-upload")
# @click.argument("agent")
# @click.argument("url")
# def url_upload(agent, url):
#     """Upload content from a URL to an agent."""
#     click.echo(f"Uploading content from {url} to agent {agent}")


# @agent.command(name="file-list")
# @click.argument("agent")
# def file_list(agent):
#     """List an agent's files."""
#     click.echo(f"Listing files for agent {agent}")


def main():
    cli(auto_envvar_prefix="OAICLI")


if __name__ == "__main__":
    main()
