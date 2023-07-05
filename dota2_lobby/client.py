from dota2.client import Dota2Client
from steam.client import SteamClient

# client = steam operations, dota = dota client operations
client = SteamClient()
dota = Dota2Client(client)


# starts dota client
@client.on("logged_on")
def start_dota():
    dota.launch()
