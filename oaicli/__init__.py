import os
import appdirs
from dotenv import load_dotenv
from pathlib import Path

current_working_directory = Path.cwd()
env_path = os.path.join(current_working_directory, ".env")
load_dotenv(dotenv_path=env_path)

home_dir = appdirs.user_config_dir(f"{current_working_directory}/oaicli")
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


def list_local_threads():
    # maps names to thread ids
    pass


def get_local_agents():
    # maps names to agents
    pass


def get_default():
    pass


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
