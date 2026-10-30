import asyncio
import random
import html

from telethon import events, Button
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

import env
from Hack import bot
from Hack.helpers import MENU1, KEYBOARD1
from Hack.database import DB


PHOTO_URL = "https://i.ibb.co/DgC1fvDm/ylr-RIOh9.jpg"

SUPPORT_LINK = "https://t.me/lynx_madara"
DEVELOPER_LINK = "https://t.me/seximadara"

WELCOME_BUTTONS = [
    [Button.inline("ʜαᴄκ ѕєѕѕɪση", data=b"show_hack")],
    [
        Button.url("ѕυᴘᴘσʀᴛ", SUPPORT_LINK),
        Button.url("∂єᴠєʟσᴘєʀ", DEVELOPER_LINK),
    ],
]

_GREET = ["💞", "🥂", "🔍", "🧪", "⚡", "🔥"]


async def _play_intro(message):
    """Reaction → greet → Ding Dong animation → delete."""

    try:
        await bot(
            SendReactionRequest(
                peer=message.chat_id,
                msg_id=message.id,
                reaction=[ReactionEmoji(emoticon="🥰")],
            )
        )
    except Exception:
        pass

    loading_1 = None

    try:
        loading_1 = await message.reply(random.choice(_GREET))

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ᴅɪηɢ ᴅᴏηɢ.❤️‍🔥</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ᴅɪηɢ ᴅᴏηɢ..❤️‍🔥</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ᴅɪηɢ ᴅᴏηɢ...</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ϻα∂αʀα</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ϻα∂αʀα x</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>ϻα∂αʀα x ѕᴛʀɪηɢ ʜαᴄκ</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)
        await loading_1.edit(
            "<blockquote><b>sᴛᴧʀᴛed!🥀</b></blockquote>",
            parse_mode="html",
        )

        await asyncio.sleep(0.1)

    except Exception:
        pass

    if loading_1:
        try:
            await loading_1.delete()
        except Exception:
            pass


def _welcome_text(user):
    full_name = " ".join(
        part for part in [
            getattr(user, "first_name", None),
            getattr(user, "last_name", None),
        ] if part
    ) or "User"

    user_id = getattr(user, "id", None)

    if user_id:
        name = (
            f'<a href="tg://user?id={user_id}">'
            f'{html.escape(full_name)}</a>'
        )
    else:
        name = html.escape(full_name)

    return (
        "<blockquote><b>"
        "<emoji id=6177168011175138815>💎</emoji> ʜєʏ " + name + " ! "
        "<emoji id=6294262456185265300>😽</emoji>\n\n"
        "<emoji id=5978869985299142389>🦋</emoji> ᴡєʟᴄσϻє ᴛσ "
        "𝐒ᴛʀɪɴɢ 𝐇ᴀᴄᴋ ꭙ 𝐁ᴏᴛ ⚡ "
        "<emoji id=6073117703965511893>💐</emoji>\n"
        "ᴘʀєϻɪυϻ • ғαѕᴛ • ѕϻσσᴛʜ\n\n"
        "<emoji id=5411472846645914012>🎁</emoji> "
        "α ᴘσωєʀғυʟ ʜαᴄᴋɪηɢ ᴛσσʟ ʙσᴛ ғσʀ ᴛєʟєɢʀαϻ\n\n"
        "<emoji id=4956250031741993892>⚡</emoji> ɪηѕᴛαηᴛ ʀєѕᴘσηѕє\n"
        "<emoji id=4956371914323920049>🔄</emoji> ѕϻσσᴛʜ ᴘєʀғσʀϻαηᴄє\n"
        "<emoji id=4958479549265347295>🚀</emoji> ғαѕᴛ &amp; ѕмαʀᴛ\n"
        "<emoji id=6104728985386622758>🛡️</emoji> ѕєᴄυʀє ʙσᴛ ᴇxᴘєʀɪєηᴄє\n\n"
        "<emoji id=4958665796227171144>💡</emoji> "
        "ѕєη∂ <b>/hack</b> ᴛσ σᴘєη ᴛнє мєηυ\n\n"
        "<emoji id=6269140848873574815>❤️</emoji> ᴘσᴡєʀєᴅ ʙʏ : "
        "<a href='https://t.me/seximadara'>𝐌ᴀᴅᴀʀᴀ</a>\n\n"
        "•── ⋅ ⋅ ────── ⋅᯽⋅ ────── ⋅ ⋅ ──•"
        "</b></blockquote>"
    )


@bot.on(events.NewMessage(pattern=r"^/start(?:\s|$)"))
async def start(event):
    user_id = event.sender_id
    sender = await event.get_sender()

    await _play_intro(event.message)

    welcome = _welcome_text(sender)

    try:
        await bot.send_file(
            event.chat_id,
            PHOTO_URL,
            caption=welcome,
            parse_mode="html",
            spoiler=True,
            buttons=WELCOME_BUTTONS,
        )
    except Exception:
        await event.reply(
            welcome,
            buttons=WELCOME_BUTTONS,
            parse_mode="html",
        )

    if DB:
        try:
            await DB.add_user(user_id)
        except Exception:
            pass

        if env.LOG_GROUP_ID:
            try:
                user = sender
                username_str = (
                    f"@{user.username}" if user.username else "None"
                )

                user_mention = (
                    f'<a href="tg://user?id={user.id}">'
                    f'{html.escape(user.first_name or "User")}</a>'
                )

                await bot.send_message(
                    env.LOG_GROUP_ID,
                    (
                        "<blockquote>📝 "
                        "<b>ʜᴀᴄᴋ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ</b>\n\n"
                        f"👤 <b>ᴜsᴇʀ ɴᴀᴍᴇ :</b> {user_mention}\n"
                        f"🍂 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{user.id}</code>\n"
                        f"🔐 <b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                        f"{html.escape(username_str)}</blockquote>"
                    ),
                    parse_mode="html",
                )
            except Exception:
                pass


@bot.on(events.CallbackQuery(data=b"show_hack"))
async def show_hack(event):
    await event.answer()
    await event.respond(
        MENU1,
        buttons=KEYBOARD1,
        parse_mode="html",
    )


@bot.on(events.NewMessage(pattern=r"^/hack(?:\s|$)"))
async def hack(event):
    if not event.is_private:
        return await event.reply(
            "<blockquote><b>ᴘʟєαsє υsє мє ɪη ᴘʀɪᴠαтє ᴄʜαт.</b></blockquote>",
            parse_mode="html",
        )

    await event.reply(
        MENU1,
        buttons=KEYBOARD1,
        parse_mode="html",
    )
