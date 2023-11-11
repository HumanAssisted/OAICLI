import os
import appdirs
from dotenv import load_dotenv

# Example using appdirs for cross-platform compatibility
home_dir = appdirs.user_config_dir("oaicli")
agents_dir = os.path.join(home_dir, "agents")
os.makedirs(agents_dir, exist_ok=True)
threads_dir = os.path.join(home_dir, "threads")
os.makedirs(threads_dir, exist_ok=True)
files_dir = os.path.join(home_dir, "files")
os.makedirs(files_dir, exist_ok=True)


env_path = os.path.join(home_dir, ".env")
load_dotenv(dotenv_path=env_path)

# Now you can access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_local_threads():
    pass


def get_local_agents():
    pass
