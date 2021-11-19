
from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from handlers import __version__
from helpers.decorators import sudo_users_only
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **[Wᴇʟᴄᴏᴍᴇ](https://te.legra.ph/file/a045aefa994cd73320fa0.jpg) {message.from_user.mention()} !**\n
🔥 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Cᴀɴ Pʟᴀʏ Mᴜsɪᴄ Iɴ Yᴏᴜʀ Oᴘ Gʀᴏᴜᴩ Vᴏɪᴄᴇ Cʜᴀᴛ💖. Dᴇᴠᴇʟᴏᴩᴇᴅ Bʏ [AɱαɳッGυʝʝαɾ](https://t.me/DARKAMAN) !**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "『 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 』",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("『 𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴 』", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("『 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂 』", callback_data="cbcmds"),
                    InlineKeyboardButton("『 𝙲𝚁𝙴𝙰𝚃𝙴𝚁 』", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "『 𝚂𝚄𝙿𝙿𝙾𝚁𝚃 』", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "『 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 』", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )

@Client.on_message(
    command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **ʜᴇʟʟᴏ** {message.from_user.mention()} !
» **press the button below to read the explanation and see the list of available commands !**
⚡ __𝙿𝙾𝚆𝙴𝚁𝙴𝙳 𝙱𝚈 {BOT_NAME} 𝙰.𝙸__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="『 𝙱𝙰𝚂𝙸𝙲 𝙶𝚄𝙸𝙳𝙴 』", callback_data="cbguide")]]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("`〘 ♕ ᑭσɳց! ♕ 〙`\n" f"〘🔥`{delta_ping * 1000:.3f} ms`〙")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
