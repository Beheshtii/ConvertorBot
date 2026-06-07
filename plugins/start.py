from pyrogram import Client, filters
from pyrogram.types import Message
from handlers import *

@Client.on_message(filters.command('start'), filters.user(ADMINS))
async def start_handler(client: Client, message: Message):
    global ADMIN_DATA
    chat_id = message.chat.id

    if chat_id in ADMIN_DATA:
        set_admin_data(chat_id)
        await message.reply_text('☀️ ویدیو رو بفرست تا به ویدیو مسیج تبدیلش کنم\n.', quote=True)


