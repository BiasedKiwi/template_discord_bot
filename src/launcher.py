import logging
import os
from datetime import datetime
from pathlib import Path
import discord
from dotenv import load_dotenv
from rich.console import Console
from rich.traceback import install

from bot import load_config, Bot


install(show_locals=True, suppress=[discord])
console = Console()
console.rule("[yellow bold]LOADING", characters="=")

now = datetime.now()

logger = logging.getLogger("discord")
conf = load_config()

TOKEN = ""
INTENTS = None
IGNORED_EXTENSIONS = []

# If you would like to edit these values, use the config.yaml file in ./bot/config.yaml
PREFIX = ""
LOG_LEVEL = ""
DEBUG_EVENTS = ""


def configure_logger():
    global LOG_LEVEL
    global DEBUG_EVENTS

    path = (
        Path(__file__).parent.parent / f"logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )

    handler = logging.FileHandler(
        filename=path.absolute(),
        encoding="utf-8",
        mode="w",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(module)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    if conf["debug_logs"]:
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

    if conf["clean_logs"]:
        directory = "../logs"
        files = os.listdir(directory)
        log_files = sorted(
            [f for f in files if f.endswith(".log") and f != ".gitkeep"],
            key=lambda f: os.path.getmtime(os.path.join(directory, f)),
        )

        files_to_keep = log_files[-conf["keep_logs"] :] + [".gitkeep"]
        files_to_delete = [f for f in files if f not in files_to_keep]

        for file_to_delete in files_to_delete:
            os.remove(os.path.join(directory, file_to_delete))


def get_token():
    load_dotenv()
    token = os.environ.get("TOKEN")
    if token is None:
        print(
            "Please provide a valid Discord API token. You can set an environment variable 'TOKEN' to allow the bot to access the token."
        )
        while (
            True
        ):  # If the program was executed from a binary, keep the terminal window alive.
            pass

    global TOKEN
    TOKEN = token


def set_intents():
    global IGNORED_EXTENSIONS
    global INTENTS

    if not conf["load_debug_cogs"]:
        IGNORED_EXTENSIONS = conf["debug_cogs"]
    else:
        IGNORED_EXTENSIONS = []

    INTENTS = discord.Intents.default()
    INTENTS.message_content = True
    INTENTS.voice_states = True

    return INTENTS


def get_prefix():
    global PREFIX

    PREFIX = conf["prefix"]

    return PREFIX


if __name__ == "__main__":
    try:
        configure_logger()
        logging_setup = True
    except Exception:
        console.log(
            "[red]ERROR: An error occured while trying to setup logging. This can be safely ignored."
        )
        logging_setup = False
    get_token()
    set_intents()

    instance = Bot(
        command_prefix=get_prefix(),
        intents=set_intents(),
        strip_after_prefix=True,
        case_insensitive=True,
        enable_debug_events=DEBUG_EVENTS,
        ignore_cogs=IGNORED_EXTENSIONS,
    )  # Initialise a bot instance
    try:
        if logging_setup:
            instance.run(TOKEN, log_level=LOG_LEVEL)
        else:
            instance.run(TOKEN)
    except KeyboardInterrupt:
        logger.info("")
    except discord.errors.LoginFailure:
        logger.critical("Login failure, an improper token was passed. Aborting.")
