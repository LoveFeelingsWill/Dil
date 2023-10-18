from pyrogram import Client
from pyrogram.types import ChatPermissions
from YukkiMusic import app as Celestia


SUDO_USERS = [6280048819, 6691393517, 5465943450]

promote_privileges = ChatPermissions(
    can_change_info=True,
    can_invite_users=True,
    can_delete_messages=True,
    can_restrict_members=True,
    can_pin_messages=True,
    can_promote_members=False,
    can_manage_chat=True,
    can_manage_video_chats=True,
)

demote_privileges = ChatPermissions(
    can_change_info=False,
    can_invite_users=False,
    can_delete_messages=False,
    can_restrict_members=False,
    can_pin_messages=False,
    can_promote_members=False,
    can_manage_chat=False,
    can_manage_video_chats=False,
)

@Celestia.on_message(filters.command("elestia", prefixes=["c", "C"]) & filters.user(OWNER_ID))
async def restriction_celestia(celestia: Client, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if data:
        user_id = reply.from_user.id if reply else None

        for action in data:
            print(f"present {action}")
            if action in "promote":
                if user_id:
                    await celestia.promote_chat_member(chat_id, user_id, privileges=promote_privileges)
                    await message.reply("OK, sir promoted!")

            elif action in "demote":
                if user_id:
                    await celestia.promote_chat_member(chat_id, user_id, privileges=demote_privileges)
                    await message.reply("OK, sir demoted!")

            elif action in "ban":
                if user_id:
                    if user_id in SUDO_USERS:
                        await message.reply("i can't ban my sudo users ")
                    else:
                        await celestia.ban_chat_member(chat_id, user_id)
                        await message.reply("OK, banned!")

            elif action in "unban":
                if user_id:
                    await celestia.unban_chat_member(chat_id, user_id)
                    await message.reply("OK, unbanned!")

            elif action in "kick":
                if user_id:
                    if user_id in SUDO_USERS:
                        await message.reply("i can't kick my sudo users")
                    else:
                        await celestia.kick_chat_member(chat_id, user_id)
                        await message.reply("Get lost! Bhaga diya bhosdi wale ko")

            elif action in "mute":
                if user_id:
                    if user_id in SUDO_USERS:
                        await message.reply("i can't mute my sudo users")
                    else:
                        permissions = ChatPermissions(can_send_messages=False)
                        await message.chat.restrict_member(user_id, permissions)
                        await message.reply("Muted successfully! Disgusting people.")

            elif action in "unmute":
                if user_id:
                    permissions = ChatPermissions(can_send_messages=True)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply("Huh, OK, sir!")





