
import env
import asyncio
from Hack import bot
from Hack.database import DB

from telethon import events, errors


@bot.on(events.NewMessage(pattern=r"/broadcast\s*([\s\S]*)?"))
async def broadcast(event):
    if not DB:
        await event.reply(
            "<blockquote><b>ᴘʟєαѕє α∂∂ мσηɢσ υʀʟ ғɪʀѕᴛ</b></blockquote>",
            parse_mode="html"
        )
        return

    if not (event.sender_id in env.SUDOERS):
        return

    text = event.pattern_match.group(1)
    reply = await event.get_reply_message()

    if not (text or reply):
        return await event.reply(
            "<blockquote><b>ᴘʟєαѕє ɢɪᴠє α ᴛєхᴛ σʀ ʀєᴘʟʏ ᴛσ α мєѕѕαɢє</b></blockquote>",
            parse_mode="html"
        )

    sent = 0
    ids = await DB.get_users()

    msg = await event.reply(
        "<blockquote><b>ᴘʀσᴄєѕѕɪηɢ....\nᴘʟєαѕє ∂ση'ᴛ ∂єℓєᴛє ᴛʜє ʀєᴘʟɪє∂ мєѕѕαɢє</b></blockquote>",
        parse_mode="html"
    ) if reply else await event.reply(
        "<blockquote><b>ᴘʀσᴄєѕѕɪηɢ....</b></blockquote>",
        parse_mode="html"
    )

    for user in ids:
        try:
            await reply.forward_to(user) if reply else await bot.send_message(
                user, text, parse_mode="html"
            )
            sent += 1
            await asyncio.sleep(0.8)
        except errors.rpcerrorlist.FloodWaitError as fwerr:
            await asyncio.sleep(fwerr.seconds + 5)
        except Exception:
            continue

    result = (
        f"<blockquote><b>ʙʀσα∂ᴄαѕᴛє∂ ɪη {len(ids)} ᴄʜαᴛѕ\n"
        f"ѕυᴄᴄєѕѕғυʟ: {sent}</b></blockquote>"
    )

    try:
        await msg.edit(result, parse_mode="html")
    except Exception:
        await event.reply(result, parse_mode="html")
        
