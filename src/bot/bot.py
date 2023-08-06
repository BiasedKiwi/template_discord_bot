# pylint: disable=missing-class-docstring
from pathlib import Path
from pkgutil import iter_modules
from subprocess import run

try:
    # Non-standard imports go here
    from discord.ext import commands
    from rich.console import Console
except ImportError:
    # This should only be used on client machines since directly using `pip install` can mess with Pipenv environments.
    prompt = input("Missing libraries, would you like to install them now? (Y/n): ")
    if prompt.lower() == "y" or prompt == "":
        run(
            [
                "python",
                "-m",
                "pip",
                "install",
                "-r",
                Path(__file__).parent.parent.parent / "requirements.txt",
            ]
        )

console = Console()


class Bot(commands.AutoShardedBot):
    """Bot instance"""

    def __init__(self, **kwargs):
        self.case_insensitive = True
        self.strip_after_prefix = True
        self.ignore_cogs = kwargs["ignore_cogs"]
        super().__init__(**kwargs)

    async def setup_hook(self):
        # Code here run after the bot has logged in, but before it has connected to the Websocket.
        await self.load_cogs()

    async def load_cogs(self) -> None:
        ext_path = Path(__file__).parent / "./extensions"
        all_extensions = [
            m.name for m in iter_modules([str(ext_path)], prefix="bot.extensions.")
        ]
        for ext in all_extensions:
            await self.load_extension(ext)


if __name__ == "__main__":
    console.print(
        "Please launch the [link=../../../launcher.py]launcher.py[/] file instead of this one directly."
    )
