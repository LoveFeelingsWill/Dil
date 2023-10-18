
import re
from pyrogram import filters
from database.filters_db import (
    delete_filter,
    get_filter,
    get_filters_names,
    save_filter,
)
from YukkiMusic import app
from misskaty.core.decorator.errors import capture_err
from misskaty.core.decorator.permissions import adminsOnly
from misskaty.core.keyboard import ikb
from misskaty.helper.functions import extract_text_and_keyb



@app.on_message(filters.command(["addfilter", "filter"]) & ~filters.private)
@adminsOnly("can_change_info")
async def save_filters(_, m):
    if len(m.command) == 1 or not m.reply_to_message:
        return await m.reply_msg(
            "**Usage:**\nReply to a text or sticker with /addfilter [FILTER_NAME] to save it.",
            del_in=6,
        )
    if not m.reply_to_message.text and not m.reply_to_message.sticker:
        return await m.reply_msg(
            "__**You can only save text or stickers in filters for now.**__"
        )
    name = m.text.split(None, 1)[1].strip()
    if not name:
        return await m.reply_msg("**Usage:**\n__/addfilter [FILTER_NAME]__", del_in=6)
    chat_id = m.chat.id
    _type = "text" if m.reply_to_message.text else "sticker"
    _filter = {
        "type": _type,
        "data": m.reply_to_message.text.markdown
        if _type == "text"
        else m.reply_to_message.sticker.file_id,
    }
    await save_filter(chat_id, name, _filter)
    await m.reply_msg(f"__**Saved filter {name}.**__")
    await m.stop_propagation()


@app.on_message(filters.command("filters") & ~filters.private)
async def get_filterss(_, m):
    _filters = await get_filters_names(m.chat.id)
    if not _filters:
        return await m.reply_msg("**No filters in this chat.**")
    _filters.sort()
    msg = f"List of filters in {m.chat.title} - {m.chat.id}\n"
    for _filter in _filters:
        msg += f"**-** `{_filter}`\n"
    await m.reply_msg(msg)


@app.on_message(filters.command(["stop", "stopfilter"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_filter(_, m):
    if len(m.command) < 2:
        return await m.reply_msg("**Usage:**\n__/stopfilter [FILTER_NAME]__", del_in=6)
    name = m.text.split(None, 1)[1].strip()
    if not name:
        return await m.reply_msg("**Usage:**\n__/stopfilter [FILTER_NAME]__", del_in=6)
    chat_id = m.chat.id
    deleted = await delete_filter(chat_id, name)
    if deleted:
        await m.reply_msg(f"**Deleted filter {name}.**")
    else:
        await m.reply_msg("**No such filter.**")
    await m.stop_propagation()


@app.on_message(
    filters.text & ~filters.private & ~filters.via_bot & ~filters.forwarded,
    group=-3,
)
async def filters_re(_, message):
    text = message.text.lower().strip()
    if not text:
        return
    chat_id = message.chat.id
    list_of_filters = await get_filters_names(chat_id)
    for word in list_of_filters:
        pattern = r"( |^|[^\w])" + re.escape(word) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            _filter = await get_filter(chat_id, word)
            data_type = _filter["type"]
            data = _filter["data"]
            if data_type == "text":
                keyb = None
                if re.findall(r"\[.+\,.+\]", data):
                    if keyboard := extract_text_and_keyb(ikb, data):
                        data, keyb = keyboard

                if message.reply_to_message:
                    await message.reply_to_message.reply(
                        data,
                        reply_markup=keyb,
                        disable_web_page_preview=True,
                    )

                    if text.startswith("~"):
                        await message.delete()
                    return

                return await message.reply(
                    data,
                    reply_markup=keyb,
                    quote=True,
                    disable_web_page_preview=True,
                )
            if message.reply_to_message:
                await message.reply_to_message.reply_sticker(data)

                if text.startswith("~"):
                    await message.delete()
                return
            await message.reply_sticker(data, quote=True)



                     
