import os
from dotenv import load_dotenv


load_dotenv(dotenv_path='config/config.env')

e = os.environ.get

EDIT_NOTIFICATIONS_CHANNEL_ID = e("EDIT_NOTIFICATIONS_CHANNEL_ID", 1125820992304984064)
PROGRAMMER_ROLE_ID = e("PROGRAMMER_ROLE_ID", 1126175427061371011)
