"""file with all for logs and for more clear code in main file"""
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pytz import timezone

import discord


def Kyiv_time() -> str:
    """Возвращает форматированное UTC+3 время строкой"""
    kyiv = timezone("Europe/Kiev")
    kv_time = datetime.now(kyiv)
    time_string = kv_time.strftime("%m/%d/%Y, %H:%M:%S")
    return time_string


def LogEdit(message_before: discord.Message, message_after: discord.Message) -> discord.Embed:
    """Возвращает форматированный и заполненный discord.Embed"""
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


def LogTxtEdit(message_before: discord.Message, message_after: discord.Message):
    """Создает txt файл для логирования edit message event"""
    with open("message.txt", "w") as file:
        file.write("{}\nWas changed to :\n{}".format(str(message_before.content), str(message_after.content)))
    pass


def LogTxtDelete(message):
    """Создает txt файл для логирования delete message event"""
    with open("message.txt", "w") as file:
        file.write("{}".format(str(message.content)))
    pass


def SplitEmbed() -> discord.Embed:
    """for good-looking log"""
    embed = discord.Embed(title="-------------------------------------------------------")
    return embed


def LogDelete(message: discord.Message) -> discord.Embed:
    """returns embed for Delete log"""
    embed = discord.Embed(
        title="{} has deleted message in {} text channel".format(str(message.author.name), str(message.channel.name)),
        description="",
        color=discord.Color.from_rgb(255, 0, 0),
    )
    if len(str(message.content)) < 256:
        embed.add_field(
            name=message.content,
            value="This is the message that he has deleted ",
            inline=True,
        )
    embed.add_field(name="Time: ", value=Kyiv_time())
    return embed


def LeaveLog(member) -> discord.Embed:
    """returns embed for log of leaving members from channel"""
    embed = discord.Embed(
        title="{} leaved channel at {}".format(str(member.name), Kyiv_time()), color=discord.Color.from_rgb(0, 255, 0)
    )
    return embed


def JoinLog(member) -> discord.Embed:
    """returns embed for log of joining members from channel"""
    embed = discord.Embed(
        title="{} joins channel at {}".format(str(member.name), Kyiv_time()), color=discord.Color.from_rgb(255, 255, 0)
    )
    return embed


def GifEditor(location, edited_location, guild):
    """adds current voice members and current average members"""
    frames = []
    true_member_count = len([m for m in guild.members if not m.bot])  # without bots
    voice = set()
    for v in guild.voice_channels:
        for member in v.members:
            voice.add(member.id)
    voice_member_count = len(voice)
    im = Image.open(location)
    for frame in ImageSequence.Iterator(im):
        d = ImageDraw.Draw(frame)
        ttf = ImageFont.truetype("courbi.ttf", 20)
        d.text((57, 150), str(voice_member_count), font=ttf)
        d.text((57, 185), str(true_member_count), font=ttf)
        del d
        b = BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)
    frames[0].save(edited_location, format("gif"), save_all=True, append_images=frames[1:])
    pass
