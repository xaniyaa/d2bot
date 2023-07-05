# file with all for logs for more clear text in main file
from datetime import datetime

from pytz import timezone

import discord


def Kyiv_time():  # returns UTC:+3 time
    kyiv = timezone("Europe/Kiev")
    kv_time = datetime.now(kyiv)
    time_string = kv_time.strftime("%m/%d/%Y, %H:%M:%S")
    return time_string


def LogEdit(message_before, message_after):  # returns embed for Edit log
    embed = discord.Embed(
        title=f"{message_before.author} edited his message in {message_before.channel.name} channel",
        description="",
        color=discord.Color.from_rgb(255, 0, 100),
    )
    if (
        len(str(message_before.content)) < 256 and len(str(message_after.content)) < 256
    ):  # adds pretty fields for small  embeds
        embed.add_field(name=message_before.content, value="This is the message before any edit", inline=True)
        embed.add_field(name=message_after.content, value="This is the message after the edit", inline=True)
    embed.add_field(name="Time: ", value=Kyiv_time())
    return embed


def LogTxtEdit(message_before, message_after):  # makes txt file with text more than 2000 symbols for edit log
    with open("message.txt", "w") as file:
        file.write("{}\nWas changed to :\n{}".format(str(message_before.content), str(message_after.content)))
    pass


def LogTxtDelete(message):  # makes txt file with text more than 2000 symbols for delete log
    with open("message.txt", "w") as file:
        file.write("{}".format(str(message.content)))
    pass


def SplitEmbed():  # for good-looking log
    embed = discord.Embed(title="-------------------------------------------------------")
    return embed


def LogDelete(message, deleter):  # returns embed for Delete log
    embed = discord.Embed(
        title="{} deleted a message of {} in {} text channel".format(
            str(deleter.name), str(message.author.name), str(message.channel.name)
        ),
        description="",
        color=discord.Color.from_rgb(255, 0, 0),
    )
    if len(str(message.content)) < 256:
        embed.add_field(
            name=message.content,
            value="This is the message that he has deleted ",  # adds pretty field for small  embed
            inline=True,
        )
    embed.add_field(name="Time: ", value=Kyiv_time())
    return embed


def LeaveLog(member):  # returns embed for log of leaving members from channel
    embed = discord.Embed(
        title="{} leaved channel at {}".format(str(member.name), Kyiv_time()), color=discord.Color.from_rgb(0, 255, 0)
    )
    return embed


def JoinLog(member):  # returns embed for log of joining members from channel
    embed = discord.Embed(
        title="{} joins channel at {}".format(str(member.name), Kyiv_time()), color=discord.Color.from_rgb(255, 255, 0)
    )
    return embed
