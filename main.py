import os
from discord.ext.commands.context import Context
from dotenv import load_dotenv
from discord.ext import commands
import discord

import asyncio


class MyCommandBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged in as {0} ({0.id})'.format(self.user))

    async def on_message(self, message: discord.Message):
        print(f'Message from {message.author}: {message.content}')
        await super().on_message(message)


class Greetings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def hello(self, ctx: Context, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member



async def create_bot():
    # Intents
    intents = discord.Intents.default()
    intents.message_content = True

    # Add commands by cog
    bot = MyCommandBot(command_prefix='#', intents=intents)

    await bot.add_cog( Greetings(bot) )

    return bot


def main():
    load_dotenv()

    bot = asyncio.run( create_bot() )

    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)

if __name__ == "__main__":
    main()

### repeat message ###
#導入Discord.py
import discord
#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#調用event函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：',client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果以「說」開頭
    if message.content.startswith('說'):
      #分割訊息成兩份
      tmp = message.content.split(" ",2)
      #如果分割後串列長度只有1
      if len(tmp) == 1:
        await message.channel.send("repeat message")
      else:
        await message.channel.send(tmp[1])

client.run("MTEwOTA3ODY1OTY5MzgyMTk5Mg.G06MVX.GZnFVvu5gsyFrKcBzqLDMjHjXJcDBeGCZsfFFQ")