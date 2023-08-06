# pylint: disable=W1203

import logging

from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info(f"{__name__} module loaded")

    @commands.Cog.listener()
    async def on_connect(self):
        self.logger.info("The bot has successfully connected to Discord.")

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.logger.warning(
            "The bot has disconnected from Discord. This may not be important."
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("The bot is ready for use.")
        self.logger.info(f"Command prefix: '{self.bot.command_prefix}'")

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        self.logger.debug(f"Got WebSocket event: {event_type}")

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        self.logger.debug(f"Got WebSocket message: {msg}")

    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload):
        self.logger.debug(f"Send operation done with payload: {payload}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
