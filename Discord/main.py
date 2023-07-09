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
async def on_message_delete(message):
    # on deleting message sends embed with info in log channel
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)  # log channel id
    await channel.send(embed=helpers.LogDelete(message))
    for attachment in message.attachments:
        await channel.send(attachment.url)
    if message.embeds:
        await channel.send(message.embeds)
    if len(str(message.content)) >= 2000:
        # TODO: change to Bytes.IO
        helpers.LogTxtDelete(message)
        await channel.send(file=helpers.LogTxtDelete(message).read())
    elif 2000 > len(str(message.content)) >= 256:
        await channel.send(str(message.content))
        await channel.send(embed=helpers.SplitEmbed())


@client.event
async def on_message_edit(message_before, message_after):
    # on edit message sends embed with info in log channel
    if message_before.content != message_after.content:
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
    # sends log on member join
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.LeaveLog(member))


@client.event
async def on_member_join(member):
    # sends log on member join
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.JoinLog(member))


# @tasks.loop(seconds=20.0)
# async def set_banner():
#     # Every 20 seconds changes guild banner with current number of voice members
#     # and members of channel
#     guild = client.get_guild(settings.GUILD_ID)
#     helpers.GifEditor(settings.BANNER_LOCATION, settings.EDITED_BANNER_LOCATION, guild)
#     with open(settings.EDITED_BANNER_LOCATION, 'rb') as file:
#         banner = file.read()
#     await guild.edit(banner=banner)


@client.event
async def on_member_join(member):
    # sends log on member join
    channel = client.get_channel(settings.EDIT_NOTIFICATIONS_CHANNEL_ID)
    await channel.send(embed=helpers.JoinLog(member))


@client.event
async def on_voice_state_update(member, before, after):
    if before.self_mute != after.self_mute:
        if after.self_mute:
            logger.info('{} has been muted in {}'.format(member, helpers.Kyiv_time()))
        else:
            logger.info('{} has been unmuted in {}'.format(member, helpers.Kyiv_time()))


if __name__ == "__main__":
    client.run(settings.DISCORD_API_TOKEN)
