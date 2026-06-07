from pyrogram import Client
from config import *

plugins = dict(root="plugins")


app = Client(
    name="ConvertorBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins,
)


print("Running.........")
app.run()
