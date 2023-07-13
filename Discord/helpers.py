"""file with all for logs and for more clear code in main file"""
from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageSequence
from pytz import timezone

import discord


def kyiv_time() -> str:
    """Возвращает форматированное UTC+3 время строкой"""
    kyiv = timezone("Europe/Kiev")
    kv_time = datetime.now(kyiv)
    time_string = kv_time.strftime("%m/%d/%Y, %H:%M:%S")
    return time_string


def log_edit(message_before, message_after) -> discord.Embed:
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
    embed.add_field(name="Time: ", value=kyiv_time())
    return embed


def log_txt_edit(message_before, message_after) -> BytesIO:
    """Создает txt файл для логирования edit message event"""
    message = message_before + "\nWas changed to:\n" + message_after
    bytes_message = BytesIO()
    bytes_message.write(str.encode(message))
    bytes_message.seek(0)
    return bytes_message


def log_txt_delete(message) -> BytesIO:
    """Создает txt файл для логирования delete message event"""
    bytes_message = BytesIO()
    bytes_message.write(str.encode(message))
    bytes_message.seek(0)
    return bytes_message


def split_embed() -> discord.Embed:
    """for good-looking log"""
    embed = discord.Embed(title="-------------------------------------------------------")
    return embed


def log_delete(message) -> discord.Embed:
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
    embed.add_field(name="Time: ", value=kyiv_time())
    return embed


def leave_log(member) -> discord.Embed:
    """returns embed for log of leaving members from channel"""
    embed = discord.Embed(
        title="{} leaved channel at {}".format(str(member.name), kyiv_time()), color=discord.Color.from_rgb(0, 255, 0)
    )
    return embed


def join_log(member) -> discord.Embed:
    """returns embed for log of joining members from channel"""
    embed = discord.Embed(
        title="{} joins channel at {}".format(str(member.name), kyiv_time()), color=discord.Color.from_rgb(255, 255, 0)
    )
    return embed


def gif_edit(location, edited_location, guild, x, y):
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
        d.text((x[0], y[0]), str(voice_member_count), font=ttf)
        d.text((x[1], y[1]), str(true_member_count), font=ttf)
        del d
        b = BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)
    frames[0].save(edited_location, format("gif"), save_all=True, append_images=frames[1:])


def on_mute_log(member) -> discord.Embed:
    embed = discord.Embed(title="{} has been muted at {}".format(member, kyiv_time()))
    return embed


def on_unmute_log(member) -> discord.Embed:
    embed = discord.Embed(title="{} has been unmuted at {}".format(member, kyiv_time()))
    return embed
