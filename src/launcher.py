import logging
import os
from datetime import datetime
from pathlib import Path
from subprocess import run

try:
    # Non-standard imports go here
    import discord
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.traceback import install
except ImportError:
    # This should only be used on client machines since directly using `pip install` can mess with Pipenv environments.
    prompt = input("Missing libraries, would you like to install them now? (Y/n): ")
    if prompt.lower() == "y" or prompt == "":
        run(["python", "-m", "pip", "install", "-r", Path(__file__).parent.parent.parent / 'requirements.txt'])

from bot import *

install(show_locals=True, suppress=[discord])
console = Console()
console.rule("[yellow bold]LOADING", characters="=")

now = datetime.now()

logger = logging.getLogger("discord")  # Set up logging for discord
raw_conf = get_raw_config()

handler = logging.FileHandler(
    filename=f"../logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log",
    encoding="utf-8",
    mode="w",
)
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(module)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

if raw_conf["logging"][0]["debug_logs"]:
    LOG_LEVEL = logging.DEBUG
    DEBUG_EVENTS = True
    logger.warning(
        "Debug logging is turned on. For less verbose logging, set the 'debug_logs' key in /src/bot/config.yaml to false."
    )
else:
    LOG_LEVEL = logging.INFO
    DEBUG_EVENTS = False
    logger.warning(
        "Debug logging is turned off. For more verbose logging, set the 'debug_logs' key in /src/bot/config.yaml to true"
    )
logger.setLevel(LOG_LEVEL)


# Constants
TOKEN = ""
PREFIX = ""

load_dotenv()  # Load the .env file
token = os.environ.get("TOKEN")
if token is None:  # If the token was not found in the .env file, exit the program
    print(
        "Please provide a valid Discord API token. You can set an environment variable 'TOKEN' to allow Disco Stats to access the token."
    )
    while (
        True
    ):  # If the program was executed from a binary, keep the terminal window alive.
        pass

TOKEN = token

if not raw_conf["debug"]["load_debug_cogs"]:
    ignored_cogs = raw_conf["debug"]["debug_cogs"]
else:
    ignored_cogs = []
intents = discord.Intents.default()


def set_intents():
    # pylint: disable=assigning-non-slot
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    intents.voice_states = True


instance = Bot(
    command_prefix="..",
    intents=set_intents(),
    strip_after_prefix=True,
    case_insensitive=True,
    enable_debug_events=DEBUG_EVENTS,
    ignore_cogs=ignored_cogs,
)  # Initialise a bot instance

logger.info("Welcome to Disco Stats")
try:
    instance.run(TOKEN, log_level=LOG_LEVEL)
except KeyboardInterrupt:
    logger.info("")
