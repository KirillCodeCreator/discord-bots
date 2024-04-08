import logging
import os

import discord
import requests

from config import BOT_TOKEN

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

CAT_API = "https://api.thecatapi.com/v1/images/search"
DOG_API = "https://dog.ceo/api/breeds/image/random"


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} подключился к Discord!\n'
                    f'Готов показать случайного котика (или пёсика!)')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.lower()
        cat, dog = "кот" in content, "собак" in content

        if cat or dog:
            if cat:
                r = requests.get(CAT_API)
                image_url = r.json()[0]["url"]
            else:
                r = requests.get(DOG_API)
                image_url = r.json()["message"]

            image_content = requests.get(image_url).content

            f = open(f"{os.path.basename(image_url)}", "wb")
            f.write(image_content)
            f.close()

            await message.channel.send(file=discord.File(f"{os.path.basename(image_url)}"))


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(BOT_TOKEN)
