import json
import os.path

import discord
from discord.ext import commands
from discord import app_commands

class blackListCommandGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name='blacklist', description='commands related to the blacklist')
    @app_commands.command(name='add', description='add to the blacklist')
    @app_commands.describe(serverid = 'Enter Serverid',gateid= "Enter Gate id",password='Enter password')
    async def blackList(self, interaction: discord.Interaction, serverid: str,gateid:str, password:str = None):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"You do not have enough permissions to connect.")
            return
        baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        gatePath = os.path.join(baseDir, 'database', f'{interaction.channel.id}.json')
        if not os.path.exists(gatePath):
            await interaction.followup.send(f"This channel does not have a gate yet.")
        with open(gatePath, 'r', encoding='utf-8') as f:
            data =  json.load(f)
        if not serverid.isdigit():
            await interaction.followup.send('serverid can only contain numbers')
        data['blackList'].append(serverid)
