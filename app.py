#v1.2
import os
import time
import yaml
import discord
from discord.ext import commands
from discord import SyncWebhook
#utils
from lib import Logger
from utils.sendStatics import sendStatics
#cogs
from cogs.create import createCommand
from cogs.remove import removeCommand
from cogs.connect import connect
from cogs.blackList import blackListCommandGroup
from cogs.deconnect import deconnect
#firewall
from firewall.filter import filter

app = commands.Bot(command_prefix='!', intents=discord.Intents.all())
with open('config.yml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
Logger.Info("Loading config..")
#main
main_token = data['Bot_Token']
main_language = data['language']
#statics
statisc_enable= data['Statics']['enable']
statisc_channelId= data['Statics']['channelId']
statics_sendafter= data['Statics']['sendAfter']

#firewall
blackListWord = data['blackListWord']

#in process variable
totalReq = 0
staticsMessage = None

#main vairable
startTime = time.time()

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
log_dir = os.path.join(baseDir, 'logs')
db_dir = os.path.join(baseDir, "database")
cache_dir = os.path.join(baseDir, "cache")
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    Logger.Warn("Logs path does not exist, recreating it.")
else:
    Logger.Success("Log path exists")
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)
    Logger.Warn("Database path does not exist, recreating it.")
else:
    Logger.Success("Database path exists")
if not os.path.exists(cache_dir):
    Logger.Warn("Cache path does not exist, recreating it.")
    os.makedirs(cache_dir, exist_ok=True)
else:
    Logger.Success("Cache path exists")
Logger.Info("Done...")

@app.event
async def on_ready():
    Logger.Info("Run bot...")
    Logger.Info("Sync commands")
    app.tree.add_command(createCommand())
    app.tree.add_command(blackListCommandGroup())
    await app.add_cog(removeCommand())
    await app.add_cog(connect())
    await app.add_cog(deconnect())
    await app.tree.sync()
    Logger.Info(f"Bot has run with the name {app.user}")

@app.event
async def on_message(message: discord.Message):
    #auth
    if message.author.bot:
        return
    if len(message.mentions) > 3:
        return
    if len(message.role_mentions) > 3:
        return
    #author
    Logger.Info("Get name and avatar url")
    try:
        name = message.author.name
        avatar_url = (message.author.avatar or message.author.default_avatar).url
    except Exception as e:
        Logger.Error(f"{e}")
    #check
    baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    gatePath = os.path.join(baseDir, 'database', f"{message.channel.id}.json")
    if os.path.exists(gatePath):
        global totalReq, staticsMessage
        Logger.Info(f"{message.author} -> {message.content}")
        totalReq += 1
        print(totalReq, staticsMessage)
        if statisc_enable == True:
            print('call send statics')
            await sendStatics(app=app,statisc_channelId=statisc_channelId, totalReq=totalReq,staticMessage=staticsMessage, startTime=startTime)
        else:
            pass
        with open(gatePath, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        linkList = data['linkList']
        for id in linkList:
            idGate = os.path.join(baseDir, 'database', f"{id}.json")
            if os.path.exists(idGate):
                with open(idGate, 'r', encoding='utf-8') as f:
                    idData = yaml.load(f, Loader=yaml.SafeLoader)
                if str(idData['serverId']) in data['blackList']:
                    return
                webhook = SyncWebhook.from_url(url=idData['webhookUrl'])
                if message.content.strip() == "" and message.emojis:
                    for emoji in message.emojis:
                        webhook.send(
                            username=name,
                            avatar_url=avatar_url,
                            content=emoji.url
                        )
                else:
                    content = message.content
                    content = filter(content, BlackListWord=blackListWord)
                    webhook.send(
                        username=name,
                        avatar_url=avatar_url,
                        content=content
                    )
        pass
    else:
        return
app.run(token=main_token)