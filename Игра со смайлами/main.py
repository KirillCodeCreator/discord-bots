import logging
import random

import discord

from config import BOT_TOKEN

emoji = ['🛁', '🚴', '🚀', '🚁', '🚂', '🚃', '🚌', '🚎', '🚑', '🚒', '🚓', '🦆', '🚕', '🦚', '🦞', '🚗',
         '🦑', '🚚', '🦢', '🦟', '🦠', '🦅', '🦀', '🦗', '🦋', '🚜', '🦇', '🦔', '🦓', '🚣', '🦒', '🦎',
         '🚶', '🛌', '🛒', '🛩', '🛰', '🛸', '🤔', '🤐', '🤓', '🤡', '🤫', '🥐', '🥕', '🥝', '🥦', '🥾']
score = {
    'user': 0, 'bot': 0
}

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        random.shuffle(emoji)
        if message.author == client.user:
            return
        if message.content == '/help' or message.content == '/start':
            await message.channel.send(f'Play with me in emoji! Type an integer!\nIf you want to stop type "/stop"')
        elif message.content == '/stop':
            score['user'] = 0
            score['bot'] = 0
            await message.channel.send('Buy!')
        else:
            try:
                if emoji:
                    card = int(message.content)
                    user_turn = emoji.pop(card % len(emoji))
                    bot_turn = emoji.pop(random.randint(0, 100) % len(emoji))
                    if user_turn > bot_turn:
                        score['user'] += 1
                    else:
                        score['bot'] += 1
                    await message.channel.send(f'Your emoji {user_turn}\nBot emoji {bot_turn}\n'
                                               f'Score: You {score["user"]} - Bot {score["bot"]}')
                else:
                    raise IndexError
            except IndexError:
                if score["user"] > score["bot"]:
                    await message.channel.send(f'Emoticons are over\nScore: You {score["user"]} - Bot {score["bot"]}\n'
                                               f'You win!')
                elif score["user"] < score["bot"]:
                    await message.channel.send(f'Emoticons are over\nScore: You {score["user"]} - Bot {score["bot"]}\n'
                                               f'Bot win!')
                else:
                    await message.channel.send(f'Emoticons are over\nScore: You {score["user"]} - Bot {score["bot"]}\n'
                                               f'Draw result!')
            except Exception as e:
                print(e, message.content)
                await message.channel.send('Not valid value')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(BOT_TOKEN)
