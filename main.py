### repeat message ###
#導入Discord.py
import discord
from discord import app_commands
import re, time, datetime, calendar
import func
#client 是我們與 Discord 連結的橋樑，intents 是我們要求的權限
class aclinet(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, timeout=60.0)
        self.value = None
        self.synced = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
            func.check()
            print('目前登入身份：', client.user)
        while True:
            content, name, where, who = await func.check_task()
            channel = client.get_channel(where)
            if who == "null":
                await channel.send(f'<@{name}> {content}')
            else:
                await channel.send(f'{who}來自<@{name}>的鬧鐘:\n{content}')
        
           
client = aclinet()
tree = app_commands.CommandTree(client)

@tree.command(name = "say", description = "機器人說" )
async def self(interaction: discord.Integration, echo:str, where:str="default"):
    if where == "default":
        channel = client.get_channel(interaction.channel.id)
    else:
        try:
            channel = client.get_channel(int(where))
        except:
            await interaction.response.send_message("您輸入的channel ID好像有誤, 請檢查channel ID", ephemeral=True, delete_after=10)
    
    try:
        await channel.send(echo)
        await interaction.response.send_message(echo, ephemeral=True, delete_after=3)
    except Exception as e:
        await interaction.response.send_message(echo, ephemeral=True)

@tree.command(name = "gpa", description = "請依序輸入該門課成績所對應的GPA分數及學分, 並使用','隔開" )
async def self(interaction: discord.Integration, score:str, credit:str):
    score_list = list(filter(None, re.sub(r"[^0-9.,]", "", score).split(",")))
    credit_list = list(filter(None, re.sub(r"[^0-9.,]", "", credit).split(",")))
    if len(score_list) != len(credit_list):
        title = "GPA 計算錯誤"
        msg = f"\u200b\n您輸入的GPA為: {score_list}\n您輸入的學分為{credit_list}\n請檢查漏項!\u200b\n"
    else:
        try:
            gpa = func.calculate_gpa(list(map(float, score_list)), list(map(float, credit_list)))
            gpa = round(gpa, 2)
            title = "GPA 計算結果如下"
            msg = f"\u200b\n您的學期GPA為: {gpa}!\u200b\n"
        except:
            title = "GPA 計算錯誤"
            msg = f"\u200b\n您輸入的GPA為: {score_list}\n您輸入的學分為{credit_list}\n請確認輸入!\u200b\n"

    eb = discord.Embed(title=title, description=msg)
    await interaction.response.send_message(embed = eb)

@tree.command(name = "alarm", description = "鬧鐘(time格式為24小時制, HH:MM)")
async def self(interaction: discord.Integration, mm:int, dd:int, time:str, desc:str, who:str = "default"):
    if who == "default":
        who = f"null"
    class hourErr(BaseException):
        msg = "小時請勿超過24!"
    class minErr(BaseException):
        msg = "分鐘請勿超過60!"
    toDay = datetime.datetime.now()
    nowYear = toDay.year
    try:
        checkDay = calendar.monthrange(nowYear, mm)[1]
        if dd > checkDay or not str(dd).isdigit() or dd <=0:
            raise
        if ":" in time:
            if int(time.split(":")[0]) >=24:
                raise hourErr
            if int(time.split(":")[1]) >=60:
                raise minErr
            index = func.task(mm, dd, time, desc, interaction.user.id, interaction.user,
                            interaction.guild.id, interaction.guild, interaction.guild.system_channel.id, who)
            await interaction.response.send_message(f"鬧鐘已定在{mm}/{dd}, {time}, 內容: {desc}(#{index})")
        else:
            await interaction.response.send_message("time要打':'")
    except hourErr as e:
        await interaction.response.send_message(e.msg)
    except minErr as e:
        await interaction.response.send_message(e.msg)
    except Exception as e:
        print(e)
        await interaction.response.send_message(f"無此日期{mm}/{dd}!")

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

client.run("")