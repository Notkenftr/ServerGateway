import os
import hashlib

import discord
import yaml
from discord.ext import commands
from discord import app_commands

class removeCommand(commands.Cog):
    def __init__(self):
        super().__init__()
    @app_commands.command(name='remove', description='delete gate')
    @app_commands.describe(gateid='Enter gate id (channel id)', password='Enter password')
    async def delete(self,interaction: discord.Interaction, gateid: str, password: str = None):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"You do not have enough permissions to connect.")
            return
        message =  await interaction.followup.send(f"Verifying..")
        baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        gatePath = os.path.join(baseDir, 'database', f'{gateid}.json')
        if not os.path.exists(gatePath):
            await message.edit(content=f"The gate does not exist.")
        with open(gatePath, 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        ownerId = data['ownerId']
        hashPassword = data['password']
        if not password:
            if interaction.user.id == ownerId:
                os.remove(gatePath)
                await interaction.followup.send(f"Gate has been deleted")
            else:
                await interaction.followup.send(f"You need to enter the password.")
        else:
            password = hashlib.sha512(password.encode())
            password = password.hexdigest()
            if password == hashPassword:
                os.remove(gatePath)
                await interaction.followup.send(f"Gate has been deleted")
            else:
                await interaction.followup.send(f"The password is incorrect")
