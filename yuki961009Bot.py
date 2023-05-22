import discord, os, logging, json, re
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from discord import app_commands
from discord.ui import Button, View
import time, datetime
import func

load_dotenv(r"./.env", override=True)
TOKEN = os.getenv("DiscordBotToken")

log_path = r"./bot.log"
log = logging.getLogger()
handlers = RotatingFileHandler(log_path, "a", 1024*1024*5, 3, "utf-8")
log.addHandler(handlers)
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s[%(levelname)s]%(funcName)s: %(message)s")
handlers.setFormatter(formatter)

role_msg_id=''
rec_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
rec_roles = []
sudo_id = [421904193276870657, 1013087173911785472, 564334078640259082, 582117471725682708, 618099320822169640]
jsonData = "./data.json"

class aclinet(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default(), timeout=60.0)
        self.value = None
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            logging.info(f"We have logged in as {self.user}")
            func.check()
        
client = aclinet()
tree = app_commands.CommandTree(client)

@tree.command(name = "say", description = "機器人說" )
async def self(interaction: discord.Integration, echo:str, where:str="default"):
    if interaction.user.id in sudo_id:
        if where == "default":
            channel = client.get_channel(interaction.channel.id)
        else:
            try:
                channel = client.get_channel(int(where))
            except:
                await interaction.response.send_message("您輸入的channel ID好像有誤, 請檢查channel ID", ephemeral=True, delete_after=10)
                logging.debug(f"channel ID 設定錯誤 錯誤ID為: {where}")
        
        try:
            eb = discord.Embed (description=f"\u200b\n　{echo}　\u200b\n\u200b\n", color=discord.Color(0xFFFFFF))
            await channel.send(embed=eb)
            await interaction.response.send_message(echo, ephemeral=True, delete_after=10)
            logging.info(f"來自 '{interaction.user}' 指令: 說 內容: {echo} 到: {where}")
        except Exception as e:
            await interaction.response.send_message(echo, ephemeral=True)
            logging.error(f"失敗。來自 '{interaction.user}' 指令: 說, 錯誤訊息: {e}")
    else:
        await interaction.response.send_message("你目前尚未有權限", ephemeral=True, delete_after=5)
        logging.info(f"失敗。來自 '{interaction.user}' 指令: say, 沒有權限")

@tree.command(name = "sendimg", description = "輸入圖片的url" )
async def self(interaction: discord.Integration, url:str, where:str="default"):
    if interaction.user.id in sudo_id:
        if where == "default":
            channel = client.get_channel(interaction.channel.id)
        else:
            try:
                channel = client.get_channel(int(where))
            except:
                await interaction.response.send_message("您輸入的channel ID好像有誤, 請檢查channel ID", ephemeral=True, delete_after=10)
                logging.debug(f"channel ID 設定錯誤 錯誤ID為: {where}")
        
        try:
            eb = discord.Embed()
            eb.set_image(url=url)
            await channel.send(embed=eb)
            await interaction.response.send_message(url, ephemeral=True, delete_after=10)
            logging.info(f"來自 '{interaction.user}' 指令: 說 內容: {url} 到: {where}")
        except Exception as e:
            await interaction.response.send_message(url, ephemeral=True)
            logging.error(f"失敗。來自 '{interaction.user}' 指令: 說, 錯誤訊息: {e}")
    else:
        await interaction.response.send_message("你目前尚未有權限", ephemeral=True, delete_after=5)
        logging.info(f"失敗。來自 '{interaction.user}' 指令: sendimg, 沒有權限")

@tree.command(name = "addroles", description = "依照順序輸入你想要給的身分組(上限為10個)\nexample: @admin @guset(用空格分隔身分組)")
async def self(interaction: discord.Integration, roles:str, title:str="自訂義title", where:str="default"):
    global role_msg_id, rec_emoji, rec_roles
    rec_roles = []
    temp = []
    msg = f"\u200b\n　‧{title}　\n\n"
    
    if interaction.user.id in sudo_id:
        if where == "default":
            channel = client.get_channel(interaction.channel.id)
        else:
            try:
                channel = client.get_channel(int(where))
            except:
                await interaction.response.send_message("您輸入的channel ID好像有誤, 請檢查channel ID", ephemeral=True, delete_after=10)
                logging.debug(f"channel ID 設定錯誤 錯誤ID為: {where}")

        total_roles = re.findall(r"<@&.*?>", roles)
        total_roles_len = len(total_roles)

        for role, emoji in zip(total_roles, rec_emoji):
            role_obj = discord.utils.get(interaction.guild.roles, id=func.extract_role_id(role))
            if role_obj is None:
                await interaction.response.send_message(
                    f"找不到名稱為 `{role}` 的身分組", ephemeral=True, delete_after=10
                )
                return
            
            temp.append(role)
            temp.append(emoji)
            msg += "　‧ {}　".format(role)
            rec_roles.append(temp)
            temp = []
        msg += "\u200b\n\u200b\n"
        eb = discord.Embed (description=msg, color=discord.Color(0xFFFFFF))
        await interaction.response.send_message("Ok!", ephemeral=True, delete_after=5)
        sendMsg = await channel.send(embed = eb)
        role_msg_id = sendMsg.id

        with open(jsonData, "r") as f:
            data = json.load(f)

        data["data"].append({"msg_id": role_msg_id, "roles": rec_roles})

        with open(jsonData, "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)
        
        for index in range(total_roles_len):
            if index < len(rec_emoji):
                await sendMsg.add_reaction(rec_emoji[index])
    else:
        await interaction.response.send_message("你目前尚未有權限", ephemeral=True, delete_after=5)
        logging.info(f"失敗。來自 '{interaction.user}' 指令: addroles, 沒有權限")

@tree.command(name = "ping", description = "就ping")
async def self(interaction: discord.Integration):
    if interaction.user.id in sudo_id:
        await interaction.response.send_message(f'Pong! {round(client.latency * 1000, 2)}ms.')
        logging.info(f"來自 '{interaction.user}' 指令: ping")
    else:
        await interaction.response.send_message("你目前尚未有權限", ephemeral=True, delete_after=5)
        logging.info(f"失敗。來自 '{interaction.user}' 指令: ping, 沒有權限")

@tree.command(name = "help", description = "就help")
async def self(interaction: discord.Integration):
    if interaction.user.id in sudo_id:
        msg = '`/addrules`\n\
傳送一個embed 依照點擊的emoji增加身分組\n\
roles 必填: 請依序填入身分組, 中間以空格分隔\n\
title 選填: 如未輸入embed第一行會顯示 "自定義title"\n\
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel\n\
\n\
`/say`\n\
輸入想說的話, 機器人會幫你傳送到想要的頻道\n\
echo 必填: 輸入想要說的話\n\
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel\n\
\n\
`/ping`\n\
顯示伺服器的連線延遲狀況\n\
\n\
`/sendimg`\n\
傳送圖片(輸入url)\n\
url 必填: 輸入圖片網址\n\
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel\n\
\n\
`/help`\n\
使用說明\
'
        await interaction.response.send_message(f'{msg}', ephemeral=True)
        logging.info(f"來自 '{interaction.user}' 指令: ping")
    else:
        await interaction.response.send_message("你目前尚未有權限", ephemeral=True, delete_after=5)
        logging.info(f"失敗。來自 '{interaction.user}' 指令: help, 沒有權限")

@client.event
async def on_raw_reaction_add(payload):
    global role_msg_id, rec_roles

    with open("./data.json", "r") as f:
        data = json.load(f)
    message_id = payload.message_id
    for index in range(len(data["data"])):
        if message_id == data["data"][index]["msg_id"] and payload.member.id != client.user.id:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

            for roles in data["data"][index]["roles"]:
                try:
                    role, emoji = roles
                    if payload.emoji.name == emoji:
                        add_role = discord.utils.get(guild.roles, id=func.extract_role_id(role))
                except Exception as e:
                    logging.error(e)

            if add_role is not None:
                await payload.member.add_roles(add_role)
                logging.info(f"已為{payload.member.name}添加: {add_role} 身分組")

client.run(TOKEN)