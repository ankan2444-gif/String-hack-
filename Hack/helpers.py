import base64
import struct
import asyncio
import ipaddress
import requests as r

from Hack import bot
from logger import LOGGER
from traceback import format_exc
from env import LOG_GROUP_ID, MUST_JOIN, DISABLED

from telethon import errors, Button
from telethon.events import CallbackQuery
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.sessions.string import _STRUCT_PREFORMAT, CURRENT_VERSION, StringSession
from telethon.errors.rpcerrorlist import UserNotParticipantError, UserIsBlockedError


MENU1 = """<blockquote><b>
𝗔 - ᴄʜєᴄк υѕєʀ σωη ɢʀσυᴘѕ αη∂ ᴄʜαηηєʟѕ(ᴘυвʟɪᴄ σηʟʏ)

𝗕 - ᴄʜєᴄк υѕєʀ αʟʟ ɪηғσʀмαᴛɪση ʟɪкє ᴘʜσηє ηυмвєʀ, υѕʀηαмє... єᴛᴄ

𝗖 - вαη αʟʟ ᴛʜє мємвєʀѕ ғʀσм ᴛʜє ɢʀσυᴘ

𝗗 - кησω υѕєʀ ʟαѕᴛ σᴛᴘ, υѕє σᴘᴛɪση в ғɪʀѕᴛ ᴛσ ᴛαкє ηυмвєʀ ᴛʜєη ʟσɢɪη

𝗘 - ᴊσɪη α ɢʀσυᴘ/ᴄʜαηηєʟ/ʟɪηк νɪα ѕᴛʀɪηɢѕєѕѕɪση

𝗙 - ʟєανє α ɢʀσυᴘ/ᴄʜαηηєʟ νɪα ѕᴛʀɪηɢѕєѕѕɪση

𝗚 - ∂єʟєᴛє α ɢʀσυᴘ/ᴄʜαηηєʟ

𝗛 - ᴄʜєᴄк υѕєʀ ᴛωσ ѕᴛєᴘ ɪѕ єηαвʟє σʀ ∂ɪѕαвʟє
</b></blockquote>"""

MENU2 = """<blockquote><b>
𝗜 - ᴛєʀмɪηαᴛє αʟʟ ᴄυʀʀєηᴛ αᴄᴛɪνє ѕєѕѕɪσηѕ єхᴄєᴘᴛ ʏσυʀ ѕᴛʀɪηɢѕєѕѕɪση

𝗝 - ∂єʟєᴛє αᴄᴄσυηᴛ

𝗞 - ʟєανє αʟʟ ɢʀσυᴘѕ/ᴄʜαηηєʟѕ

𝗟 - вʀσα∂ᴄαѕᴛ вυᴛᴛσηѕ

𝗠 - ᴛєʀмɪηαᴛє ᴄυʀʀєηᴛ ѕєѕѕɪση

𝗡 - ɪηνɪᴛє αʟʟ

𝗢 - ∂ємσᴛє α мємвєʀ

𝗣 - ᴘʀσмσᴛє α мємвєʀ
</b></blockquote>"""

BROADCAST_BUTTONS = [[
    Button.inline("Group", data="1"),
    Button.inline("User", data="2"),
], [
    Button.inline("All", data="3"),
]]

BROADCAST_OPTION = {
    b"1": {
        "group": True
    },
    b"2": {
        "user": True
    },
    b"3": {
        "group": True,
        "user": True
    }
}

KEYBOARD1 = [
    [
        Button.inline("A", data="A"),
        Button.inline("B", data="B"),
        Button.inline("C", data="C"),
        Button.inline("D", data="D")
    ],
    [
        Button.inline("E", data="E"),
        Button.inline("F", data="F"),
        Button.inline("G", data="G"),
        Button.inline("H", data="H")
    ],
    [
        Button.inline("𝗡𝗘𝗫𝗧 ⏭️", data="next")
    ]
]

KEYBOARD2 = [
    [
        Button.inline("I", data="I"),
        Button.inline("J", data="J"),
        Button.inline("K", data="K"),
        Button.inline("L", data="L")
    ],
    [
        Button.inline("M", data="M"),
        Button.inline("N", data="N"),
        Button.inline("O", data="O"),
        Button.inline("P", data="P")
    ],
    [
        Button.inline("𝗕𝗔𝗖𝗞 ⏮️", data="back")
    ]
]


async def join_checker(e):
    if not MUST_JOIN:
        return True
    chat = await bot.get_entity(MUST_JOIN)
    try:
        await bot(GetParticipantRequest(chat, e.sender_id))
        return True
    except UserNotParticipantError:
        join_chat = f"https://t.me/{chat.username}"
        button = [[
            Button.url(text="Join", url=join_chat),
        ]]

        TEXT = "<blockquote><b>ʜєʏ ʟσσкѕ ʟɪкє ʏσυ ʜανєη'ᴛ ᴊσɪη συʀ ᴄʜαᴛ ʏєᴛ, ᴘʟєαѕє ᴊσɪη ғɪʀѕᴛ!</b></blockquote>"

        await bot.send_message(e.sender_id, TEXT, buttons=button, parse_mode="html")

        return False
    except Exception as err:
        LOGGER(__name__).error(err)
        return True


def paste(text):
    link = 'https://spaceb.in/'
    url = 'https://spaceb.in/api/v1/documents'
    payload = {"content": text, "extension": "txt"}
    headers = {
        "Content-Type": "application/json"
    }

    response = r.post(url, json=payload, headers=headers)
    hash = response.json().get('payload').get('id')

    return link + hash



def on_callback(data=None):
    def dec(func):
        async def wrap(e):
            # Answer the callback promptly to reduce expired-query errors.
            try:
                await e.answer()
            except errors.QueryIdInvalidError:
                return
            except Exception as callback_error:
                LOGGER(__name__).warning(
                    "Callback answer failed: %s",
                    type(callback_error).__name__,
                )

            try:
                check = await join_checker(e)
                if not check:
                    return

                if func.__name__ in DISABLED:
                    await e.answer(
                        "This function is currently disabled",
                        alert=True,
                    )
                    return

                await func(e)

            except errors.common.AlreadyInConversationError:
                try:
                    await e.answer(
                        "A conversation is already active. Finish it first.",
                        alert=True,
                    )
                except Exception:
                    pass

            except (asyncio.CancelledError, UserIsBlockedError):
                return

            except Exception as err:
                error_text = (
                    f"Callback: {func.__name__}\n"
                    f"Error: {type(err).__name__}: {err}\n\n"
                    f"{format_exc()}"
                )

                LOGGER(__name__).error(error_text)

                # Do not send session strings, tokens, or API credentials
                # to third-party paste services.
                if LOG_GROUP_ID:
                    try:
                        await bot.send_message(
                            LOG_GROUP_ID,
                            "<blockquote><b>Callback error occurred. "
                            "Check the VPS logs for details.</b></blockquote>",
                            parse_mode="html",
                        )
                    except Exception as log_error:
                        LOGGER(__name__).warning(
                            "Could not send error notice: %s",
                            type(log_error).__name__,
                        )

                try:
                    await e.respond(
                        "<blockquote><b>ѕσмє єʀʀσʀ σᴄᴄυʀʀє∂. "
                        "ᴘʟєαѕє ᴄʜєᴄκ ᴛʜє ʙσᴛ ℓσɢѕ.</b></blockquote>",
                        parse_mode="html",
                    )
                except Exception as reply_error:
                    LOGGER(__name__).warning(
                        "Could not send error reply: %s",
                        type(reply_error).__name__,
                    )

        bot.add_event_handler(wrap, CallbackQuery(data=data))
        return wrap

    return dec



# https://github.com/TeamUltroid/Ultroid/blob/main/pyUltroid/startup/connections.py

_PYRO_FORM = {351: ">B?256sI?", 356: ">B?256sQ?", 362: ">BI?256sQ?"}

DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def validate_session(session):
    # Telethon Session
    if session.startswith(CURRENT_VERSION):
        if len(session.strip()) != 353:
            return False
        return StringSession(session)

    # Pyrogram Session
    elif len(session) in _PYRO_FORM.keys():
        if len(session) in [351, 356]:
            dc_id, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        else:
            dc_id, _, _, auth_key, _, _ = struct.unpack(
                _PYRO_FORM[len(session)],
                base64.urlsafe_b64decode(session + "=" *
                                         (-len(session) % 4)),
            )
        return StringSession(CURRENT_VERSION + base64.urlsafe_b64encode(
            struct.pack(
                _STRUCT_PREFORMAT.format(4),
                dc_id,
                ipaddress.ip_address(DC_IPV4[dc_id]).packed,
                443,
                auth_key,
            )).decode("ascii"))
    else:
        return False
        
