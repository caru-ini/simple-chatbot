# Chat module for the bot
from typing import Optional

import openai
from discord import Message

from dotenv import load_dotenv
from pathlib import Path
import os
from logging import getLogger

logger = getLogger(__name__)

load_dotenv()

CHAT_MODEL = os.getenv('CHAT_MODEL', 'gpt-4-turbo-preview')
ASK_MODEL = os.getenv('ASK_MODEL', 'gpt-4-turbo-preview')
SUMMARY_MODEL = os.getenv('SUMMARY_MODEL', 'gpt-3.5-turbo-16k')

chat_prompt = Path('./prompts/chat.txt').read_text(encoding='utf-8')
ask_prompt = Path('./prompts/ask.txt').read_text(encoding='utf-8')
summary_prompt = Path('./prompts/summary.txt').read_text(encoding='utf-8')


# check key decorator
def check_openai_key(func):
    async def wrapper(*args, **kwargs):
        if not os.getenv('OPENAI_API_KEY'):
            raise Exception('OpenAI API Key not found')
        return await func(*args, **kwargs)

    return wrapper


class ChatBot:
    def __init__(self, channel_id: int, bot_id: int, auto_reply=False):
        self.channel_id = channel_id
        self.bot_id = bot_id
        self.auto_reply = auto_reply
        logger.info(f'ChatBot initialised for channel_id: {channel_id} with bot_id: {bot_id}')

    @staticmethod
    @check_openai_key
    async def ask(question: str) -> str:
        logger.info(f'Ask method called with question: {question}')
        return await ChatBot.create_chat_completions(ask_prompt, [{'role': 'system', 'content': question}], model=ASK_MODEL)

    @check_openai_key
    async def summary(self, messages: list[Message]):
        logger.info(f'Summary method called with {len(messages)} messages')
        return await self.create_chat_completions(summary_prompt, self.prepare_messages(messages), model=SUMMARY_MODEL)

    @check_openai_key
    async def chat(self, messages: list[Message]) -> Optional[str]:
        logger.info(f'Chat method called with {len(messages)} messages')
        res = await self.create_chat_completions(chat_prompt, self.prepare_messages(messages), model=CHAT_MODEL)
        if res == '<END>':
            return None
        return res

    def prepare_messages(self, messages: list[Message]) -> list[dict]:
        logger.info(f'Prepare_messages method called with {len(messages)} messages')
        formatted_messages = [
            {
                'role': 'assistant' if message.author.id == self.bot_id else 'user',
                'content': f'{message.author.display_name}: {message.content}'
                if message.author.id != self.bot_id else f"{message.content}"
            }
            for message in messages
        ]
        return formatted_messages

    @staticmethod
    @check_openai_key
    async def create_chat_completions(prompt: str, messages: list[dict], model: str = CHAT_MODEL) -> str:
        logger.info(f'Create_chat_completions method called with prompt: {prompt} and {len(messages)} messages')
        # display each 10 characters of the prompt
        logger.debug(f'Messages: {[message["content"][:10] for message in messages]}')
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': prompt,
                },
                *messages,
            ],
        )
        return response.choices[0].message.content
