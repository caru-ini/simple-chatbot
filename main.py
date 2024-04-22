import asyncio
import os
from typing import Optional, Literal

from discord import Intents, Object
from dotenv import load_dotenv

from discord.ext import commands

import logging
from pathlib import Path

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
    datefmt='%X',
)
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('chat').setLevel(logging.DEBUG)
logging.getLogger('cogs.chatbot').setLevel(logging.DEBUG)
logging.getLogger('translator').setLevel(logging.DEBUG)

bot = commands.Bot(command_prefix='!', intents=Intents.all())


# Umbra's Sync Command
# Original: https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[Object],
               spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to current guild'}"
        )
        return


@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')


async def main():
    for path in Path('cogs').rglob('*.py'):
        # skip dunder files
        if path.name.startswith('__'):
            continue
        cog = '.'.join(path.with_suffix('').parts)
        try:
            await bot.load_extension(cog)
        except Exception as e:
            logging.error(f'Failed to load extension {cog}.', exc_info=e)

    try:
        await bot.start(TOKEN)
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
