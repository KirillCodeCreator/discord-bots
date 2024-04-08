import datetime
import logging

import discord

from config import BOT_TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} подключился к Discord!\n'
                    f'Отправь сообщение "set_timer in ! hours ! minutes" для установки таймераr\nЯ напомню тебе.')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        flag = False
        if message.author == client.user:
            return
        if 'help' in message.content.lower():
            await message.channel.send('Отправь сообщение "set_timer in ! hours ! minutes" для установки таймераr\nЯ напомню тебе.')
        if "set_timer" in message.content.lower():
            hours = int(message.content.lower().split()[2])
            minutes = int(message.content.lower().split()[4])
            await message.channel.send(f"The timer should start in {hours} hours and {minutes} minutes. ")
            date = datetime.datetime.now()
            delta = datetime.timedelta(hours=hours, minutes=minutes)
            flag = True

        if flag:
            while True:
                if datetime.datetime.now() > date + delta:
                    await message.channel.send(f'🕒 Time X has come')
                    flag = False
                    break


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(BOT_TOKEN)
