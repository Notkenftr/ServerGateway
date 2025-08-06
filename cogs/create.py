import os
import hashlib
import json

import discord
from discord import app_commands
from discord.ext import commands




class createCommand(app_commands.Group):
    def __init__(self):
        super().__init__(name='create', description='create command')
    @app_commands.command(name='gate-way', description='create gateway')
    @app_commands.describe(password='Enter password')
    async def createGateWay(self, interaction: discord.Interaction,password:str):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"You do not have enough permissions to connect.")
            return
        try:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            jsonPath = os.path.join(base, "database", f'{interaction.channel.id}.json')
            if os.path.exists(jsonPath):
                with open(jsonPath, 'r') as f:
                    gateData = json.load(f)
                embed = discord.Embed(
                    title='This channel had a gate before.',
                    description=f'**Infomation**\n'
                                f'> **GateId: **{gateData['channelId']}\n'
                                f'> **ownerId: **<@{gateData['ownerId']}>\n'
                                f"-# If you have admin permissions or you're the gate creator, you don't need to enter a password."
                                f'to delete the gate please use: ``/detele {gateData['channelId']} <password>``',
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return

            webhook = await interaction.channel.create_webhook(name='ServerGateWay')
            webhook = webhook.url

            password = hashlib.sha512(password.encode())
            password = password.hexdigest()
            jsonData = {
                "password": password,
                "serverId": interaction.guild.id,
                "channelId": interaction.channel.id,
                "ownerId": interaction.user.id,

                "webhookUrl": f"{webhook}",

                "linkList": [],
                "blackList": []
            }
            with open(jsonPath, 'w', encoding='utf-8') as f:
                json.dump(jsonData, f, ensure_ascii=False, indent=4)
            embed = discord.Embed(
                title='Successfully created the gate',
                description=f"**Infomation**\n"
                            f"> **GateId: ** {interaction.channel.id}\n"
                            f"> **Server Id: ** {interaction.guild.id}\n"
                            f"to connect please use: ``/connect {interaction.channel.id} <password>``",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='An error has occurred',
                description=f"```\n"
                            f"{e}\n"
                            f"```",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    @app_commands.command(name='shard', description='create a shard gateway')
    @app_commands.describe(shardname='Enter shard name')
    async def createGlobal(self, interaction: discord.Interaction, shardname: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.followup.send(f"You do not have enough permissions to connect.")
            return
        try:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            jsonPath = os.path.join(base, "shard", f'{interaction.channel.id}.json')
            if os.path.exists(jsonPath):
                with open(jsonPath, 'r') as f:
                    gateData = json.load(f)
                embed = discord.Embed(
                    title='This channel had a gate before.',
                    description=f'**Infomation**\n'
                                f'> **GateId: **{gateData['channelId']}\n'
                                f'> **ownerId: **<@{gateData['ownerId']}>\n'
                                f"-# If you have admin permissions or you're the gate creator, you don't need to enter a password."
                                f'to delete the gate please use: ``/detele {gateData['channelId']} <password>``',
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return

            webhook = await interaction.channel.create_webhook(name='ServerGateWay')
            webhook = webhook.url
            jsonData = {
                "serverId": interaction.guild.id,
                "channelId": interaction.channel.id,
                "ownerId": interaction.user.id,

                "webhookUrl": f"{webhook}",

                "linkList": [],
                "blackList": []
            }
            with open(jsonPath, 'w', encoding='utf-8') as f:
                json.dump(jsonData, f, ensure_ascii=False, indent=4)
            embed = discord.Embed(
                title='Successfully created the gate',
                description=f"**Infomation**\n"
                            f"> **GateId: ** {interaction.channel.id}\n"
                            f"> **Server Id: ** {interaction.guild.id}\n"
                            f"to connect please use: ``/connect {interaction.channel.id} <password>``",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(
                title='An error has occurred',
                description=f"```\n"
                            f"{e}\n"
                            f"```",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
