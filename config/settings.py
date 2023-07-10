import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

banner_folder_orig = os.path.join(os.path.dirname("settings.py"), "..", "static", "orig.gif")
banner_folder_image = os.path.join(os.path.dirname("settings.py"), "..", "static", "image.gif")

EDIT_NOTIFICATIONS_CHANNEL_ID = int(os.getenv("EDIT_NOTIFICATIONS_CHANNEL_ID"))
BANNER_LOCATION = os.getenv("BANNER_LOCATION", banner_folder_orig)
EDITED_BANNER_LOCATION = os.getenv("EDITED_BANNER_LOCATION", banner_folder_image)
GUILD_ID = int(os.getenv("GUILD_ID"))
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
