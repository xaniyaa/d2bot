import io

import aiohttp as aiohttp
import helpers
from apikeys import TOKEN
from loguru import logger

import discord
from config import settings
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def onready():
    logger.info("The bot is working now")
    logger.info("-------------------------------------------")


@client.event
async def on_message_delete(message):  # on deleting message sends embed with info in log channel
    async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
        deleter = entry.user
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)  # log channel id
    await channel.send(embed=helpers.LogDelete(message, deleter))

    if len(str(message.content)) >= 2000:
        # TODO: change to Bytes.IO
        helpers.LogTxtDelete(message)
        with open("message.txt", "rb") as file:
            await channel.send(file=discord.File(file, "message.txt"))

    elif 2000 > len(str(message.content)) >= 256:
        await channel.send(str(message.content))
        await channel.send(embed=helpers.SplitEmbed())


@client.event
async def on_message_edit(message_before, message_after):  # on edit message sends embed with info in log channel
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)

    is_message_too_big = len(str(message_before.content)) >= 2000 or len(str(message_after.content)) >= 2000

    if is_message_too_big:
        # if message > 2000
        helpers.LogTxtEdit(message_before, message_after)
        with open("message.txt", "rb") as file:
            await channel.send(file=discord.File(file, "message.txt"))

    elif 2000 > len(str(message_before.content)) > 256 or 2000 > len(str(message_after.content)) > 256:
        # if 2000 > message > 256
        await channel.send(str(message_before.content))
        embed = discord.Embed(title="To:")
        await channel.send(embed=embed)
        await channel.send(str(message_after.content))
        await channel.send(embed=helpers.SplitEmbed())
    else:
        # if message < 256
        await channel.send(embed=helpers.LogEdit(message_before, message_after))


@client.event
async def on_member_remove(member):
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.LeaveLog(member))


@client.command(description="Set the guild banner image")
@commands.has_role(settings.PROGRAMMER_ROLE_ID)
async def setbanner(ctx, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = io.BytesIO(await resp.read())
    await ctx.message.guild.edit(banner=data.read())
    print("done")


@client.event
async def on_member_join(member):
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.JoinLog(member))


if __name__ == "__main__":
    client.run(TOKEN)
