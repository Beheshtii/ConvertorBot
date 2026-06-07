from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from handlers import *
from uuid import uuid4
import os


@Client.on_callback_query()
async def call(client: Client, call: CallbackQuery):
    global ADMIN_DATA
    data = call.data
    msg_id = call.message.id
    chat_id = call.message.chat.id

    if data == "convert_to_video_message" and call.message.video:
        if call.message.video.duration > 60:
            await call.answer("زمان ویدیو بیشتر از یک دقیقه است ❌", show_alert=False)
            return

        if ADMINS[chat_id]["in_queue"] == True:
            await call.answer(
                "شما از قبل یک ویدیو در صف تبدیل ویدیو به ویدیو مسیج دارید, لطفا تا پایان عملیات قبلی منتظر بمانید ❣️",
                show_alert=False)
            return

        await call.answer("ویدیو درحال دانلود است لطفا صبر کنید ✅", show_alert=False)
        ADMINS[chat_id]["in_queue"] = True

        file_path = await client.download_media(
            call.message,
            file_name=f"downloads/{uuid4()}.mp4",
        )

        video_note = await client.send_video_note(chat_id=chat_id, video_note=file_path)

        await client.send_message(chat_id=chat_id,
                                  text="ویدیو با موفقیت به ویدیو مسیج تبدیل شد ✅\n.",
                                  reply_to_message_id=video_note.id)
        ADMINS[chat_id]["in_queue"] = False

        if os.path.exists(file_path):
            os.remove(file_path)

    elif data == "cancel":
        await client.delete_messages(chat_id, msg_id)
