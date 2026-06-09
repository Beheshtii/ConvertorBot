from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from handlers import *
from config import *
from uuid import uuid4
import os

app = Client(
    name="ConvertorBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

os.makedirs("downloads", exist_ok=True)

@app.on_message(filters.command('start') & filters.user(ADMINS))
async def start_handler(client: Client, message: Message):
    global ADMIN_DATA
    chat_id = message.chat.id

    set_admin_data(chat_id)

    await message.reply_text('☀️ ویدیو رو بفرست تا به ویدیو مسیج تبدیلش کنم\n.', quote=True)

@app.on_message(filters.video & filters.user(ADMINS))
async def convert_handler(client: Client, message: Message):
    global ADMIN_DATA
    chat_id = message.chat.id

    set_admin_data(chat_id)

    await client.send_video(chat_id=chat_id, video=message.video.file_id, reply_markup=convert_button)

@app.on_callback_query()
async def call(client: Client, call: CallbackQuery):
    global ADMIN_DATA
    data = call.data
    msg_id = call.message.id
    chat_id = call.message.chat.id

    set_admin_data(chat_id)

    if data == "convert_to_video_message" and call.message.video:
        if call.message.video.duration > 60:
            await call.answer("زمان ویدیو بیشتر از یک دقیقه است ❌", show_alert=False)
            return

        if ADMIN_DATA[chat_id]["in_queue"] == True:
            await call.answer(
                "شما از قبل یک ویدیو در صف تبدیل ویدیو به ویدیو مسیج دارید, لطفا تا پایان عملیات قبلی منتظر بمانید ❣️",
                show_alert=False)
            return

        await call.answer("ویدیو درحال دانلود است لطفا صبر کنید ✅", show_alert=False)
        ADMIN_DATA[chat_id]["in_queue"] = True
        file_path = None
        try:
            file_path = await client.download_media(
                call.message,
                file_name=f"downloads/{uuid4()}.mp4",
            )

            video_note = await client.send_video_note(chat_id=chat_id, video_note=file_path)

            await client.send_message(chat_id=chat_id,
                                      text="ویدیو با موفقیت به ویدیو مسیج تبدیل شد ✅\n.",
                                      reply_to_message_id=video_note.id)
        finally:
            ADMIN_DATA[chat_id]["in_queue"] = False

            if os.path.exists(file_path):
                os.remove(file_path)

    elif data == "cancel":
        await client.delete_messages(chat_id, msg_id)

print("Running.........")
app.run()
