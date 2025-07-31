import os
import json
import discord
from discord.ext import commands
from discord import app_commands


class deconnect(commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(name='deconnect', description='Disconnect this channel from a gate')
    @app_commands.describe(gateid='Gate id to disconnect from')
    async def deconnect(self, interaction: discord.Interaction, gateid: str):
        await interaction.response.defer(thinking=True)

        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send("You do not have permission to disconnect.")
            return

        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        gatePath = os.path.join(base, "database", f'{gateid}.json')

        if not os.path.exists(gatePath):
            await interaction.followup.send("The gate does not exist.")
            return

        with open(gatePath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if interaction.channel.id not in data.get('linkList', []):
            await interaction.followup.send("This channel is not connected to the gate.")
            return

        data['linkList'].remove(interaction.channel.id)

        with open(gatePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        await interaction.followup.send("Successfully disconnected this channel from the gate.")
