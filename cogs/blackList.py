import json
import os.path

import hashlib
import discord
from discord.ext import commands
from discord import app_commands

class blackListCommandGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name='blacklist', description='commands related to the blacklist')
    @app_commands.command(name='add', description='add to the blacklist')
    @app_commands.describe(serverid = 'Enter Serverid',password='Enter password')
    async def blackList(self, interaction: discord.Interaction, serverid: str, password:str = None):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"``❌`` You do not have enough permissions to connect.")
            return
        baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        gatePath = os.path.join(baseDir, 'database', f'{interaction.channel.id}.json')
        if not os.path.exists(gatePath):
            await interaction.followup.send(f"``❌`` This channel does not have a gate yet.")
            return
        with open(gatePath, 'r', encoding='utf-8') as f:
            data =  json.load(f)
        hashPassword = data['password']
        if not serverid.isdigit():
            await interaction.followup.send('``❌`` serverid can only contain numbers')
            return
        if not password:
            if interaction.user.id == data['ownerId']:
                data['blackList'].append(serverid)
                await interaction.followup.send(f"``✅`` added {serverid} to the blacklist")
            else:
                await interaction.followup.send(f"``❌`` You need to enter the password.")
        else:
            password = hashlib.sha512(password.encode())
            password = password.hexdigest()
            if password == hashPassword:
                data['blackList'].append(serverid)
                await interaction.followup.send(f"``✅``  added {serverid} to the blacklist")
            else:
                await interaction.followup.send(f"``❌``  The password is incorrect")
        with open(gatePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    @app_commands.command(name='remove', description='remove server id from the blacklist')
    @app_commands.describe(serverid = 'Enter Serverid',password='Enter password')
    async def remove(self,interaction: discord.Interaction, serverid: str, password:str =  None):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"``❌`` You do not have enough permissions to connect.")
            return
        baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        gatePath = os.path.join(baseDir, 'database', f'{interaction.channel.id}.json')
        if not os.path.exists(gatePath):
            await interaction.followup.send(f"``❌`` This channel does not have a gate yet.")
            return
        with open(gatePath, 'r', encoding='utf-8') as f:
            data =  json.load(f)
        hashPassword = data['password']
        if not serverid.isdigit():
            await interaction.followup.send('``❌`` serverid can only contain numbers')
            return
        if not password:
            if interaction.user.id == data['ownerId'] or interaction.user.guild_permissions.administrator:
                data['blackList'].remove(serverid)
                await interaction.followup.send(f'``✅`` removed {serverid} from the blacklist')
            else:
                await interaction.followup.send(f"``❌`` You need to enter the password.")
        else:
            password = hashlib.sha512(password.encode())
            password = password.hexdigest()
            if password == hashPassword:
                data['blackList'].append(serverid)
                await interaction.followup.send(f"``✅`` removed {serverid} from the blacklist")
            else:
                await interaction.followup.send(f"``❌`` The password is incorrect")
        with open(gatePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)