import asyncio
import logging

import discord
from discord.ext import commands
from translate import Translator

from config import BOT_TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class TransliteBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lang = 'en-ru'

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        await ctx.send("!!set_lang — для смены языка, пример ru-pl\n"
                       "!!text — для ввода фразы для перевода")

    @commands.command(name='set_lang')
    async def set_lang(self, ctx, lang):
        self.lang = lang
        logger.info(f'set_lang {lang}')
        await ctx.send(lang)

    @commands.command(name='text')
    async def text(self, ctx, *, text):
        languages = self.lang.split("-")
        translator = Translator(from_lang=languages[0], to_lang=languages[1])
        response = translator.translate(text)
        logger.info(f'translate {text} -> {response}')
        await ctx.send(response)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!!', intents=intents)


async def main():
    await bot.add_cog(TransliteBot(bot))
    await bot.start(BOT_TOKEN)


asyncio.run(main())
