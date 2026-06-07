from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

convert_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='تبدیل به ویدیو مسیج 🗃️', callback_data="convert_to_video_message"),
            InlineKeyboardButton(text='کنسل ❌', callback_data="cancel"),
        ]
    ]
)


def set_admin_data(chat_id):
    if chat_id not in ADMIN_DATA:
        if chat_id in ADMINS:
            ADMIN_DATA[chat_id] = {"in_queue": False}
