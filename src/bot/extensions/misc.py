# pylint: disable=W1203

import logging
from typing import Literal, Optional

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context, Greedy

from .. import gen_embed


class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.logger.info(f"{__name__} module loaded")

    @commands.command(name="sync")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Grabbed from https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#sync-command-example"""
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        # embed = gen_embed(title="Pong!", description=f"{round(self.bot.latency * 1000)}ms")
        embed = gen_embed(
            title="Pong!", description=f"{round(self.bot.latency * 1000)}ms"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Cog(bot))
