import os
import hashlib
import json
import discord
from discord.ext import commands
from discord import app_commands

class connect(commands.Cog):
    def __init__(self):
        super().__init__()
    @app_commands.command(name='connect', description='connect')
    @app_commands.describe(gateid='Gate id', password='gatePassword')
    async def connect(self,interaction: discord.Interaction,gateid: str, password: str =None):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"``❌`` You do not have enough permissions to connect.")
            return
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        localPath = os.path.join(base, "database", f'{interaction.channel.id}.json')
        gatePath = os.path.join(base, "database", f'{gateid}.json')
        if not os.path.exists(gatePath):
            await interaction.followup.send(f"``❌`` the gate does not exist")
            return
        with open(gatePath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ownerId = data['ownerId']
        hashPassword = data['password']
        if not password:
            if interaction.user.id == ownerId:
                if interaction.guild.id in data['blackList']:
                    await interaction.followup.send(f"``❌`` You are on the blacklist.")
                    return
                if interaction.channel.id in data['linkList']:
                    await interaction.followup.send(f"``❌`` you are already connected")
                    return
                data['linkList'].append(interaction.channel.id)
                await interaction.followup.send(f"``✅`` successful connection")
            else:
                await interaction.followup.send(f"``❌`` You need to enter the password.")
        else:
            password = hashlib.sha512(password.encode())
            password = password.hexdigest()
            if password == hashPassword:
                if interaction.guild.id in data['blackList']:
                    await interaction.followup.send(f"``❌`` You are on the blacklist.")
                    return
                if interaction.channel.id in data['linkList']:
                    await interaction.followup.send(f"``❌`` you are already connected")
                    return
                data['linkList'].append(interaction.channel.id)
                await interaction.followup.send(f"``✅`` successful connection")
        with open(gatePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)