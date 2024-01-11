# pylint: disable=missing-class-docstring
from pathlib import Path
from pkgutil import iter_modules

from discord.ext import commands
from rich.console import Console

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
