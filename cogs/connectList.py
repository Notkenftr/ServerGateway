import json
import os

import discord
from discord import app_commands
from discord.ext import commands

class connectList(commands.Group):
    def __init__(self):
        super().__init__()
    @app_commands.command(name='connect-list', description='Connect list')
    @app_commands.describe(gateid = "Enter gate id")
    async def connectList(self,interaction: discord.Interaction, gateid: str = None):
        await interaction.response.defer(thinking=True)
        if not gateid:
            gateid = interaction.channel.id
            baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            gatePath = os.path.join(baseDir, 'database', f"{gateid}.json")
            if not os.path.exists(gatePath):
                await interaction.followup.send(f"The gate does not exist, please enter the gate id.")
                return
            with open(gatePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            gateList = data['linkList']
            if len(gateList) < 25:
                embed = discord.Embed(
                    title=f'{gateid} gate list',
                    description='\n'.join(gateList)
                )
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f'{gateid} gate list',
                    description='\n'.join(gateList[:25])
                )
                await interaction.followup.send(embed=embed)
        else:
            baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            gatePath = os.path.join(baseDir, 'database', f"{gateid}.json")
            if not os.path.exists(gatePath):
                await interaction.followup.send(f"The gate does not exist, please enter the gate id.")
                return
            with open(gatePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if len(gateList) < 25:
                embed = discord.Embed(
                    title=f'{gateid} gate list',
                    description='\n'.join(gateList)
                )
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f'{gateid} gate list',
                    description='\n'.join(gateList[:25])
                )
                await interaction.followup.send(embed=embed)