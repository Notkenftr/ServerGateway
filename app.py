#v1.0
import os

import yaml
import discord
from discord.ext import commands
from discord import SyncWebhook
#cogs
from cogs.create import createCommand
from cogs.remove import removeCommand
from cogs.connect import connect
from cogs.blackList import blackListCommandGroup
from cogs.deconnect import deconnect
#firewal
from firewall.filter import filter

app = commands.Bot(command_prefix='!', intents=discord.Intents.all())
with open('config.yml', 'r', encoding='utf-8') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
token = data['Token']

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
db_dir = os.path.join(baseDir, "database")
os.makedirs(db_dir, exist_ok=True)


@app.event
async def on_ready():
    app.tree.add_command(createCommand())
    app.tree.add_command(blackListCommandGroup())
    await app.add_cog(removeCommand())
    await app.add_cog(connect())
    await app.add_cog(deconnect())
    await app.tree.sync()
    print(f"[+] Bot đã chạy")

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
    name = message.author.name
    avatar_url = (message.author.avatar or message.author.default_avatar).url
    #check
    baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    gatePath = os.path.join(baseDir, 'database', f"{message.channel.id}.json")
    if os.path.exists(gatePath):
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
                    content = filter(content)
                    webhook.send(
                        username=name,
                        avatar_url=avatar_url,
                        content=content
                    )
        pass
    else:
        return
app.run(token=token)