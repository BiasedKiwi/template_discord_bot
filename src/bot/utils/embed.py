from random import choice

import discord
from .. import config  # pylint: disable=no-name-in-module


def gen_embed(color: str = "default", **kwargs):
    # All built-in Discord colors
    discord_colors = {
        "blue": discord.Colour.blue(),
        "blurple": discord.Colour.blurple(),
        "brand_green": discord.Colour.brand_green(),
        "brand_red": discord.Colour.brand_red(),
        "dark_blue": discord.Colour.dark_blue(),
        "dark_embed": discord.Colour.dark_embed(),
        "dark_gold": discord.Colour.dark_gold(),
        "dark_gray": discord.Colour.dark_gray(),
        "dark_green": discord.Colour.dark_green(),
        "dark_grey": discord.Colour.dark_grey(),
        "dark_magenta": discord.Colour.dark_magenta(),
        "dark_orange": discord.Colour.dark_orange(),
        "dark_purple": discord.Colour.dark_purple(),
        "dark_red": discord.Colour.dark_red(),
        "dark_teal": discord.Colour.dark_teal(),
        "dark_theme": discord.Colour.dark_theme(),
        "darker_gray": discord.Colour.darker_gray(),
        "darker_grey": discord.Colour.darker_grey(),
        "gold": discord.Colour.gold(),
        "green": discord.Colour.green(),
        "greyple": discord.Colour.greyple(),
        "light_embed": discord.Colour.light_embed(),
        "light_gray": discord.Colour.light_gray(),
        "light_grey": discord.Colour.light_grey(),
        "lighter_gray": discord.Colour.lighter_gray(),
        "lighter_grey": discord.Colour.lighter_grey(),
        "magenta": discord.Colour.magenta(),
        "og_blurple": discord.Colour.og_blurple(),
        "orange": discord.Colour.orange(),
        "pink": discord.Colour.pink(),
        "purple": discord.Colour.purple(),
        "random": discord.Colour.random(),
        "red": discord.Colour.red(),
        "teal": discord.Colour.teal(),
        "yellow": discord.Colour.yellow(),
    }
    if color == "random":
        colour = choice(list(discord_colors.items()))[1]
        embed = discord.Embed(**kwargs, color=colour)
    else:
        try:
            colour = discord_colors[color]
        except KeyError:
            try:
                colour = int(theme[color], 16)
            except KeyError:
                colour = color
        embed = discord.Embed(**kwargs, color=colour)
    return embed


theme = config.load_theme()  # Runs on import
