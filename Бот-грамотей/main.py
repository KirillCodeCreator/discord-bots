import asyncio

import discord
import pymorphy2
from discord.ext import commands

from config import BOT_TOKEN


class TranslatorBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        message = 'Commands:\n"#!numerals" for agreement with numerals\n' \
                  '"#!alive" for define alive or not alive\n' \
                  '"#!noun" for noun case (nomn, gent, datv, accs, ablt, loct) and number state (single, plural)\n' \
                  '"#!inf" for infinitive state\n' \
                  '"#!morph" for full morphological analysis'
        await ctx.send(message)

    @commands.command(name='numerals')
    async def numerals(self, ctx, word, num):
        morph = pymorphy2.MorphAnalyzer()
        word_parse = morph.parse(word)[0].make_agree_with_number(int(num)).word
        await ctx.send(f'{num} {word_parse}')

    @commands.command(name='alive')
    async def alive(self, ctx, word):
        morph = pymorphy2.MorphAnalyzer()
        alive = morph.parse('Живое')[0]
        p = morph.parse(word)
        word_ = None
        for par in p:
            if 'NOUN' in par.tag:
                word_ = par
                break
        try:
            f = word_.tag.gender
            num = word_.tag.number
            if 'anim' in word_.tag:
                if 'plur' in word_.tag:
                    message = f'{word.capitalize()} {alive.inflect({num}).word}'
                else:
                    message = f'{word.capitalize()} {alive.inflect({f, num}).word}'
            else:
                if 'plur' in word_.tag:
                    message = f'{word.capitalize()} не {alive.inflect({num}).word}'
                else:
                    message = f'{word.capitalize()} не {alive.inflect({f, num}).word}'
        except Exception:
            message = 'Не существительное'
        await ctx.send(message)

    @commands.command(name='noun')
    async def noun(self, ctx, word, case, number):
        morph = pymorphy2.MorphAnalyzer()
        word_parse = morph.parse(word)[0]
        if 'NOUN' in word_parse[1]:
            message = word_parse.inflect({case})[0] \
                if number == 'single' else \
                word_parse.inflect({case, 'plur'})[0]
        else:
            message = f'{word.capitalize()} не существительное'
        await ctx.send(message)

    @commands.command(name='inf')
    async def infinitive(self, ctx, word):
        morph = pymorphy2.MorphAnalyzer()
        word_parse = morph.parse(word)[0]
        message = word_parse.normal_form
        await ctx.send(message)

    @commands.command(name='morph')
    async def morph(self, ctx, word):
        morph = pymorphy2.MorphAnalyzer()
        message = morph.parse(word)[0].tag.cyr_repr
        await ctx.send(message)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='#!', intents=intents)


async def main():
    await bot.add_cog(TranslatorBot(bot))
    await bot.start(BOT_TOKEN)


asyncio.run(main())
