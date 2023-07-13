import helpers
from loguru import logger

import discord
from config import settings
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    logger.info("The bot is working now")
    logger.info("-------------------------------------------")
    # set_banner.start()  # starts loop of banner updating


@client.event
async def on_message_delete(message: discord.Message):
    """Отправляет discord.Embed при удалении сообщения в логи"""
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)  # log channel id
    await channel.send(embed=helpers.log_delete(message))
    for attachment in message.attachments:
        await channel.send(attachment.url)
    if message.embeds:
        await channel.send(embeds=message.embeds)
        await channel.send(embed=helpers.split_embed())
    if len(str(message.content)) >= 2000:
        await channel.send(file=discord.File(helpers.log_txt_delete(str(message.content)), "message.txt"))
    elif 2000 > len(str(message.content)) >= 256:
        await channel.send(str(message.content))
        await channel.send(embed=helpers.split_embed())


@client.event
async def on_message_edit(message_before: discord.Message, message_after: discord.Message):
    """Отправляет discord.Embed при изменении сообщения в логи"""
    if message_before.content != message_after.content:
        channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)

        is_message_too_big = len(str(message_before.content)) >= 2000 or len(str(message_after.content)) >= 2000

        if is_message_too_big:
            # if message > 2000
            helpers.log_txt_edit(message_before, message_after)
            with open("message.txt", "rb") as file:
                await channel.send(file=discord.File(file, "message.txt"))

        elif 2000 > len(str(message_before.content)) > 256 or 2000 > len(str(message_after.content)) > 256:
            # if 2000 > message > 256
            await channel.send(str(message_before.content))
            embed = discord.Embed(title="To:")
            await channel.send(embed=embed)
            await channel.send(str(message_after.content))
            await channel.send(embed=helpers.split_embed())
        else:
            # if message < 256
            await channel.send(embed=helpers.log_edit(message_before, message_after))


@client.event
async def on_member_remove(member):
    """Логирует выходы пользователей на сервер"""
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.leave_log(member))


@client.event
async def on_member_join(member):
    """Логирует заходы пользователей на сервер"""
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.join_log(member))


@tasks.loop(seconds=20.0)
async def set_banner():
    # Every 20 seconds changes guild banner with current number of voice members
    # and members of channel
    guild = client.get_guild(settings.GUILD_ID)
    helpers.gif_edit(
        settings.BANNER_LOCATION, settings.EDITED_BANNER_LOCATION, guild, settings.COORDINATES_X, settings.COORDINATES_Y
    )
    with open(settings.EDITED_BANNER_LOCATION, "rb") as file:
        banner = file.read()
    await guild.edit(banner=banner)


@client.event
async def on_voice_state_update(member, before, after):
    # sends logs about self_mute status
    if before.self_mute != after.self_mute:
        channel = client.get_channel(settings.MICROPHONE_LOGS_CHANNEL)
        if after.self_mute:
            await channel.send(embed=helpers.on_mute_log(member))
        else:
            await channel.send(embed=helpers.on_unmute_log(member))


if __name__ == "__main__":
    client.run(settings.DISCORD_API_TOKEN)
