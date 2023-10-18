from pyrogram import filters 
from functools import partial, wraps
from pyrogram.types Message
from traceback import format_exc as err
from pyrogram.errors import ChatWriteForbidden
from typing import Optional, Union


SUDO = [6280048819, 6691393517, 5465943450] 

async def member_permissions(chat_id: int, user_id: int, client):
    perms = []
    try:
        member = (await client.get_chat_member(chat_id, user_id)).privileges
        if member.can_post_messages:
            perms.append("can_post_messages")
        if member.can_edit_messages:
            perms.append("can_edit_messages")
        if member.can_delete_messages:
            perms.append("can_delete_messages")
        if member.can_restrict_members:
            perms.append("can_restrict_members")
        if member.can_promote_members:
            perms.append("can_promote_members")
        if member.can_change_info:
            perms.append("can_change_info")
        if member.can_invite_users:
            perms.append("can_invite_users")
        if member.can_pin_messages:
            perms.append("can_pin_messages")
        if member.can_manage_video_chats:
            perms.append("can_manage_video_chats")
        return perms
    except:
        return []



async def authorised(func, subFunc2, client, message, *args, **kwargs):
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await message.chat.leave()
    except Exception as e:
        try:
            await message.reply_text(str(e.MESSAGE))
        except AttributeError:
            await message.reply_text(str(e))
        e = err()
        print(e)
    return subFunc2


async def unauthorised(message: Message, permission, subFunc2):
    text = f"You don't have the required permission to perform this action.\n**Permission:** __{permission}__"
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await message.chat.leave()
    return subFunc2


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc2(client, message: Message, *args, **kwargs):
            chatID = message.chat.id
            if not message.from_user:
                # For anonymous admins
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func,
                        subFunc2,
                        client,
                        message,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(message, permission, subFunc2)
            # For admins and sudo users
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID, client)
            if userID not in SUDO and permission not in permissions:
                return await unauthorised(message, permission, subFunc2)
            return await authorised(func, subFunc2, client, message, *args, **kwargs)

        return subFunc2

    return subFunc




