from client import dota
from client import client
import logging
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/config.env")

username = os.getenv("account_username")
password = os.getenv("account_password")
print(username, password)


# creates lobby and make bot join specs
def create_practice_lobby():
    dota.destroy_lobby()
    dota.create_practice_lobby(
        password="5454",
        options=dict(
            game_name="test1",
            pass_key="5454",
            server_region=8,
            game_mode=2,
            pause_setting=0,
        ),
    )
    dota.join_practice_lobby_broadcast_channel(channel=1)


if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(name)s: %(message)s", level=logging.DEBUG)
    dota.on("ready", create_practice_lobby)
    client.cli_login(username=username, password=password)
    client.run_forever()
