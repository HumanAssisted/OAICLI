import os
import appdirs
from dotenv import load_dotenv
from pathlib import Path
import click
import requests
from mimetypes import guess_extension
import re
import shutil

current_working_directory = Path.cwd()
env_path = os.path.join(current_working_directory, ".env")
load_dotenv(dotenv_path=env_path)

OAICLI_HOME = ".oaicli"

home_dir = appdirs.user_config_dir(f"{current_working_directory}/{OAICLI_HOME}")
agents_dir = os.path.join(home_dir, "agents")
os.makedirs(agents_dir, exist_ok=True)
threads_dir = os.path.join(home_dir, "threads")
os.makedirs(threads_dir, exist_ok=True)
FILES_DIR = os.path.join(home_dir, "files")
os.makedirs(FILES_DIR, exist_ok=True)


DEFAULT_MODEL = "gpt-4-1106-preview"
DEFAULT_IMAGE_MODEL = "gpt-4-1106-vision-preview"

# Now you can access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_MODEL_TYPE = os.getenv("OPEN_AI_MODEL_TYPE", DEFAULT_MODEL)
OPEN_AI_VISION_MODEL_TYPE = os.getenv("OPEN_AI_VISION_MODEL_TYPE", DEFAULT_IMAGE_MODEL)
DEFAULT_ALLOWED_EXTENSIONS = [
    ".doc",
    ".txt",
    ".md",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
]


# use with @click.argument('file_path', type=FilePathParamType())
class FilePathParamType(click.Path):
    def shell_complete(self, ctx, param, incomplete):
        return [
            click.shell_completion.Candidate(e)
            for e in os.listdir(".")
            if e.startswith(incomplete)
        ]


# use with prompt click.prompt('Please enter a file path', type=FilePathType())
class FilePathType(click.Path):
    def convert(self, value, param, ctx):
        if not os.path.exists(value):
            self.fail(f"The file path '{value}' does not exist.", param, ctx)
        return super().convert(value, param, ctx)


def is_url(string):
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:\S+(?::\S*)?@)?"  # optional username:password@
        r"(?:"  # domain...
        r"(?P<private_ip>10(?:\.\d{1,3}){3})"  # ...including private & local networks
        r"|"
        r"(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-4])))"
        r"|"
        r"(?P<local_host>localhost)"  # localhost...
        r"|"
        r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"  # ...or domain
        r"(?:[a-zA-Z]{2,})"  # TLD
        r")"
        r"(?::\d{2,5})?"  # optional port
        r"(?:/\S*)?"  # optional path
        r"$"
    )
    return re.match(url_regex, string) is not None


def copy_file(filepath, allowed_extensions=DEFAULT_ALLOWED_EXTENSIONS):
    """
    Given a local filesystem filepath, copy, get the filename, and filename
    extension and copy the contents to FILES_DIR
    """
    # Check that the file exists
    filepath = filepath.strip()
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return

    # Determine the filename from the path
    filename = os.path.basename(filepath)

    # Determine the file extension
    _, ext = os.path.splitext(filename)

    # Check if the file extension is allowed
    if ext.lower() not in allowed_extensions:
        print(f"File extension '{ext}' not allowed.")
        return

    # Define the destination path
    file_path = os.path.join(FILES_DIR, filename)

    # Copy the file contents to the destination
    try:
        shutil.copy(filepath, file_path)
        print(f"File copied to {file_path}")
    except Exception as e:
        print(f"Failed to copy file: {e}")
        return

    return file_path, filename


def download_file(url, allowed_extensions=DEFAULT_ALLOWED_EXTENSIONS):
    # Determine the file extension
    response = requests.head(url)
    content_type = response.headers.get("content-type")
    ext = guess_extension(content_type)

    # Check if the file extension is allowed
    if ext not in allowed_extensions:
        print(f"File extension '{ext}' not allowed.")
        return

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        # Extract filename and ensure it's valid
        filename = url.split("/")[-1]
        if not filename:
            print("Could not determine filename.")
            return

        file_path = os.path.join(FILES_DIR, filename)

        # Write the file to the specified directory
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"File downloaded successfully to {file_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
    return file_path, filename


ASCII_ART = """

      ___           ___                       ___
     /  /\\         /  /\\        ___          /  /\\                      ___
    /  /::\\       /  /::\\      /  /\\        /  /:/                     /  /\\
   /  /:/\\:\\     /  /:/\\:\\    /  /:/       /  /:/       ___     ___   /  /:/
  /  /:/  \\:\\   /  /:/~/::\\  /__/::\\      /  /:/  ___  /__/\\   /  /\\ /__/::\\
 /__/:/ \\__\\:\\ /__/:/ /:/\\:\\ \\__\\/\\:\\__  /__/:/  /  /\\ \\  \\:\\ /  /:/ \\__\\/\\:\\__
 \\  \\:\\ /  /:/ \\  \\:\\/:/__\\/    \\  \\:\\/\\ \\  \\:\\ /  /:/  \\  \\:\\  /:/     \\  \\:\\/\\
  \\  \\:\\  /:/   \\  \\::/          \\__\\::/  \\  \\:\\  /:/    \\  \\:\\/:/       \\__\\::/
   \\  \\:\\/:/     \\  \\:\\          /__/:/    \\  \\:\\/:/      \\  \\::/        /__/:/
    \\  \\::/       \\  \\:\\         \\__\\/      \\  \\::/        \\__\\/         \\__\\/
     \\__\\/         \\__\\/                     \\__\\/
"""
