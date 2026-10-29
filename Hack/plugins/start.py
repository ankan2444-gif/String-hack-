
import asyncio
import random
import html

from telethon import events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

import env
from Hack import bot
from Hack.helpers import MENU1, KEYBOARD1
from Hack.database import DB


PHOTO_URL = "https://i.ibb.co/DgC1fvDm/ylr-RIOh9.jpg"

_GREET = ["💞", "🥂", "🔍", "🧪", "⚡", "🔥"]


async def _play_intro(message):
    """Reaction → greet → Ding Dong animation → delete."""

    # ── REACTION START ──────────────────────────────────
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
    # ── REACTION END ────────────────────────────────────

    # ── WRITING ANIMATION ───────────────────────────────
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
            "<blockquote><b>ᴅɪηɢ ᴅᴏηɢ...❤️‍🔥</b></blockquote>",
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

    # ── DELETE ANIMATION ────────────────────────────────
    if loading_1:
        try:
            await loading_1.delete()
        except Exception:
            pass




def _welcome_text(user):
    full_name = " ".join(
        part for part in [user.first_name, user.last_name] if part
    ) or "User"

    name = (
        f'<a href="tg://user?id={user.id}">'
        f'{html.escape(full_name)}</a>'
    )

    return (
        "<blockquote><b>"
        f"<emoji id=6177168011175138815>💎</emoji> ʜєʏ {name} ! "
        "<emoji id=6294262456185265300>😽</emoji>\n\n"
        "<emoji id=5978869985299142389>🦋</emoji> ᴡєʟᴄσϻє ᴛσ "
        "<b>𝐒ᴛʀɪɴɢ 𝐇ᴀᴄᴋ ꭙ 𝐁ᴏᴛ ⚡</b> "
        "<emoji id=6073117703965511893>💐</emoji>\n"
        "ᴘʀєϻɪυϻ • ғαѕᴛ • ѕϻσσᴛʜ\n\n"
        "<emoji id=5411472846645914012>🎁</emoji> "
        "α ᴘσωєʀғυʟ ʜαᴄᴋɪɴɢ ᴛσσʟ ʙσᴛ ғσʀ ᴛєʟєɢʀαϻ\n\n"
        "<emoji id=4956250031741993892>⚡</emoji> ɪηѕᴛαηᴛ ʀєѕᴘσηѕє\n"
        "<emoji id=4956371914323920049>🔄</emoji> ѕϻσσᴛʜ ᴘєʀғσʀϻαηᴄє\n"
        "<emoji id=4958479549265347295>🚀</emoji> ғαѕᴛ &amp; ѕмαʀᴛ\n"
        "<emoji id=6104728985386622758>🛡️</emoji> ѕєᴄυʀє ʙσᴛ ᴇxᴘєʀɪєηᴄє\n\n"
        "<emoji id=4958665796227171144>💡</emoji> "
        "ѕєη∂ <b>/hack</b> ᴛσ σᴘєη ᴛнє мєηυ\n\n"
        "<emoji id=6269140848873574815>❤️</emoji> ᴘσᴡєʀє∂ ʙʏ : "
        "<a href='https://t.me/seximadara'>𝐌ᴀᴅᴀʀᴀ</a>\n\n"
        "•── ⋅ ⋅ ────── ⋅᯽⋅ ────── ⋅ ⋅ ──•"
        "</b></blockquote>"
    )

@bot.on(events.NewMessage(pattern=r"^/start(?:\s|$)"))
async def start(event):
    user_id = event.sender_id
    sender = await event.get_sender()
    first_name = sender.first_name or "User"

    # Reaction and animation
    await _play_intro(event.message)


    # Welcome message with spoiler photo
    welcome = _welcome_text(first_name)

    try:
        await bot.send_file(
            event.chat_id,
            PHOTO_URL,
            caption=welcome,
            parse_mode="html",
            spoiler=True,
        )
    except Exception:
        await event.reply(welcome, parse_mode="html")

    # Add user to database
    if DB:
        try:
            await DB.add_user(user_id)
        except Exception:
            pass


        # Log new user
        if env.LOG_GROUP_ID:
            try:
                user = await event.get_sender()
                username_str = f"@{user.username}" if user.username else "None"
                user_mention = f'<a href="tg://user?id={user.id}">{html.escape(user.first_name or "User")}</a>'

                await bot.send_message(
                    env.LOG_GROUP_ID,
                    (
                        f"<blockquote>📝 <b>ʜᴀᴄᴋ ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ</b>\n\n"
                        f"👤 <b>ᴜsᴇʀ ɴᴀᴍᴇ :</b> {user_mention}\n"
                        f"🍂 <b>ᴜsᴇʀ ɪᴅ :</b> <code>{user.id}</code>\n"
                        f"🔐 <b>ᴜsᴇʀɴᴀᴍᴇ :</b> {html.escape(username_str)}</blockquote>"
                    ),
                    parse_mode="html",
                )
            except Exception:
                pass

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
    
