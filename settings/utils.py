from aiogram import types, Bot
from aiogram.utils.media_group import MediaGroupBuilder


import segno
import io




async def delete_media_group(cb: types.CallbackQuery, bot: Bot):
    await bot.delete_message(chat_id=cb.from_user.id,
                                message_id=cb.message.message_id)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-1)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-2)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-3)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-4)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-5)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-6)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-7)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-8)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-9)
    await bot.delete_message(chat_id=cb.from_user.id,
                            message_id=cb.message.message_id-10)
            



async def generate_qrcode(payload: str, format: str = "PNG") -> types.BufferedInputFile:
    qrcode = segno.make_qr(content=payload, error="H")
    buffer = io.BytesIO()

    with buffer as f:     
        qrcode.save(f, kind=format, scale=10)
        buffer.seek(0)
        
        return types.BufferedInputFile(buffer.read(), filename='image.png')



async def create_media_group(caption, list_img_ids: list[str]):
    media_group = MediaGroupBuilder(caption=caption)
    for img_id in list_img_ids:
        media_group.add_photo(media=img_id)

    return media_group.build()


