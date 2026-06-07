from pyrogram import Client, filters
from pyrogram.types import Message
from handlers import *

@Client.on_message(filters.video, filters.user(ADMINS))
async def convert_handler(client: Client, message: Message):
    global ADMIN_DATA
    chat_id = message.chat.id

    await client.send_video(chat_id=chat_id, video=message.video.file_id, reply_markup=convert_button)