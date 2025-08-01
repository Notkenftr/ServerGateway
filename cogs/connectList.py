import discord
from discord import app_commands
from discord.ext import commands

class connectList(commands.Group):
    def __init__(self):
        super().__init__()
    @app_commands.command(name='connect-list', description='Connect list')
    async def connectList(self):
        pass