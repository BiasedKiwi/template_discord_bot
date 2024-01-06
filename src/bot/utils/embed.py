import discord
from .. import config


def gen_embed(color: str = "default", **kwargs):
    colour = int(theme[color], 16)
    embed = discord.Embed(**kwargs, color=colour)
    return embed

theme = config.load_theme()  # Runs on import
