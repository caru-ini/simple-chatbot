# Chat Bot Cog
import logging
from typing import Optional

from discord import Message, Embed, Colour, app_commands
from discord.ext import commands
from chat import ChatBot

logger = logging.getLogger(__name__)


class ChatBotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(self.bot, 'chatbots'):
            self.bot.chatbots = {
                # channel_id: ChatBot
            }

    def get_chatbot(self, channel_id: int) -> ChatBot:
        if channel_id not in self.bot.chatbots:
            self.bot.chatbots[channel_id] = ChatBot(channel_id, self.bot.user.id)
        return self.bot.chatbots[channel_id]

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        chatbot = self.get_chatbot(message.channel.id)
        if chatbot.auto_reply or self.bot.user.mentioned_in(message):
            async with message.channel.typing():
                history = [v async for v in message.channel.history(limit=10, oldest_first=True, before=message)]
                history.append(message)
                response = await chatbot.chat(history)
                await message.channel.send(response)

    @commands.hybrid_command(
        description="Chat with the bot",
    )
    @app_commands.describe(
        message="The message to send to the bot",
        window="The number of messages to include in the chat history"
    )
    async def chat(self, ctx: commands.Context, message: str, window: Optional[int] = 10):
        await ctx.interaction.response.defer()

        messages = [ctx.message]
        if window > 0:
            messages.append(v async for v in ctx.channel.history(limit=window, oldest_first=True, before=ctx.message))

        chatbot = self.get_chatbot(ctx.channel.id)
        response = await chatbot.chat(messages)
        await ctx.send(response)

    @commands.hybrid_command(
        description="Ask the bot a question",
        aliases=["qa"]
    )
    @app_commands.describe(
        question="The question to ask the bot",
        private="Whether to send the response in a private message"
    )
    async def ask(self, ctx: commands.Context, question: str, private: Optional[bool] = False):
        await ctx.interaction.response.defer(ephemeral=True)
        chatbot = self.get_chatbot(ctx.channel.id)
        response = await chatbot.ask(question)
        embed = Embed(color=Colour.dark_gray()).add_field(name="Answer", value=response)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        description="Summarize the chat history",
    )
    @app_commands.describe(
        window="The number of messages to include in the summary",
        private="Whether to show the summary only to you"    
    )
    async def summary(self, ctx: commands.Context, window: Optional[int] = 50, private: Optional[bool] = False):
        await ctx.interaction.response.defer(ephemeral=True)
        messages = [v async for v in ctx.channel.history(limit=window, oldest_first=True, before=ctx.message)]
        chatbot = self.get_chatbot(ctx.channel.id)
        response = await chatbot.summary(messages)
        embed = Embed(color=Colour.dark_gray()).add_field(name="Summary", value=response)
        return await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        description="Enable or disable auto-reply in the channel",
        aliases=["ar"]
    )
    @app_commands.describe(enabled="Whether to enable or disable auto-reply Empty to toggle")
    async def auto_reply(self, ctx: commands.Context, enabled: Optional[bool]):
        chatbot = self.get_chatbot(ctx.channel.id)
        if isinstance(enabled, bool):
            chatbot.auto_reply = enabled
        else:
            chatbot.auto_reply = not chatbot.auto_reply
        await ctx.send("Auto-reply is now " + ("enabled" if chatbot.auto_reply else "disabled"), ephemeral=True)

    @commands.hybrid_command()
    @app_commands.describe(length="The number of messages to include in the auto-reply window")
    async def auto_reply_window(self, ctx: commands.Context, length: Optional[int]):
        chatbot = self.get_chatbot(ctx.channel.id)
        if isinstance(length, int):
            chatbot.auto_reply_window = length
        await ctx.send(f"Auto-reply window is now {chatbot.auto_reply_window}", ephemeral=True)

    @commands.is_owner()
    @commands.hybrid_command(description="Purge messages in the channel")
    @app_commands.describe(limit="The number of messages to delete")
    async def purge(self, ctx: commands.Context, limit: int = 1):
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f"Deleted {len(deleted)} messages", ephemeral=True)

    @chat.error
    @ask.error
    @summary.error
    @auto_reply.error
    async def on_chat_error(self, ctx: commands.Context, error: Exception):
        logger.error(f"Error in {ctx.command.qualified_name}: {error}")
        await ctx.send(embed=Embed(title="Error", description=str(error), color=Colour.red()), ephemeral=True)


async def setup(bot):
    await bot.add_cog(ChatBotCog(bot))
