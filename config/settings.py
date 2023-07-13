import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SETTINGS_PATH = Path("settings.py")
STATIC_PATH = SETTINGS_PATH.parent / ".." / "static"

BANNER_FOLDER_ORIG = STATIC_PATH / "orig.gif"
BANNER_FOLDER_IMAGE = STATIC_PATH / "image.gif"
EDIT_NOTIFICATIONS_CHANNEL_ID = int(os.getenv("EDIT_NOTIFICATIONS_CHANNEL_ID"))
BANNER_LOCATION = os.getenv("BANNER_LOCATION", BANNER_FOLDER_ORIG)
EDITED_BANNER_LOCATION = os.getenv("EDITED_BANNER_LOCATION", BANNER_FOLDER_IMAGE)
GUILD_ID = int(os.getenv("GUILD_ID"))
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
MICROPHONE_LOGS_CHANNEL = int(os.getenv("MICROPHONE_LOGS_CHANNEL"))
COORDINATES_X = [57, 57]
COORDINATES_Y = [165, 185]
