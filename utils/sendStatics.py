import psutil, os, datetime
import discord
from discord.ext import commands

async def sendStatics(app, statisc_channelId, totalReq, staticMessage):
    if totalReq % 100 == 0 and totalReq != 0:
        staticChannel = app.get_channel(statisc_channelId)
        process = psutil.Process(os.getpid())
        ramUsage = process.memory_info().rss / 1024 / 1024
        if staticChannel:
            embed = discord.Embed(
                title='Server Gate way Statics',
                description='**Infomation**\n'
                            f'> **Total req:** {totalReq}\n'
                            f'> **Uptime:** {str(datetime.timedelta(seconds=int(time.time() - startTime)))}\n'
                            f'> **Memory usage:** ``{round(ramUsage, 2)}`` mb',
                color=discord.Color.green()
            )
            if staticMessage:
                await staticMessage.edit(embed=embed)
            else:
                staticMessage = await staticChannel.send(embed=embed)
        else:
             return