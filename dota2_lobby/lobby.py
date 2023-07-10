import logging
import os

from client import client, dota
from dotenv import load_dotenv

username = os.getenv("ACCOUNT_USERNAME")
password = os.getenv("ACCOUNT_PASSWORD")


# creates lobby and make bot join specs
def create_practice_lobby():
    """creates dota 2 lobby"""
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
