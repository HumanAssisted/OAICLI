import click


@click.group()
def cli():
    """Main entry point for oaicli."""
    pass


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
@click.argument("agent_name")
def create_agent(agent_name):
    """Create a new agent."""
    click.echo(f"Creating agent: {agent_name}")


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
