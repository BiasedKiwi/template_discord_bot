import discord
from .. import config  # pylint: disable=no-name-in-module


def gen_embed(color: str = "default", **kwargs):
    colour = int(theme[color], 16)
    embed = discord.Embed(**kwargs, color=colour)
    return embed


theme = config.load_theme()  # Runs on import
