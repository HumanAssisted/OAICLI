import os
import appdirs
from dotenv import load_dotenv
from pathlib import Path
import click

current_working_directory = Path.cwd()
env_path = os.path.join(current_working_directory, ".env")
load_dotenv(dotenv_path=env_path)

OAICLI_HOME = ".oaicli"

home_dir = appdirs.user_config_dir(f"{current_working_directory}/{OAICLI_HOME}")
agents_dir = os.path.join(home_dir, "agents")
os.makedirs(agents_dir, exist_ok=True)
threads_dir = os.path.join(home_dir, "threads")
os.makedirs(threads_dir, exist_ok=True)
files_dir = os.path.join(home_dir, "files")
os.makedirs(files_dir, exist_ok=True)


DEFAULT_MODEL = "gpt-4-1106-preview"
DEFAULT_IMAGE_MODEL = "gpt-4-1106-vision-preview"

# Now you can access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_AI_MODEL_TYPE = os.getenv("OPEN_AI_MODEL_TYPE", DEFAULT_MODEL)
OPEN_AI_VISION_MODEL_TYPE = os.getenv("OPEN_AI_VISION_MODEL_TYPE", DEFAULT_IMAGE_MODEL)


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
