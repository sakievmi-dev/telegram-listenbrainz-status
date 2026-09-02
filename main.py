import asyncio
import logging
import os
import json
import sys

from aiogram.types import InputMediaPhoto
import liblistenbrainz

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import settings

dispatcher = Dispatcher()
listen_brainz = liblistenbrainz.ListenBrainz()

CWD = os.getcwd()
PERSISTS_FILE_PATH = CWD + "/persists.json"

text = ""
old_text = ""


async def get_message_text(listen: liblistenbrainz.Listen | None) -> str:
    if listen and listen.artist_name and listen.track_name:
        return settings.TEXT_TEMPLATE.replace(
            "[txthere]", f"{listen.artist_name} — {listen.track_name}"
        )

    return settings.TEXT_TEMPLATE.replace("[txthere]", "Nothing is playing right now.")


async def get_listen_cover_url(listen: liblistenbrainz.Listen | None) -> str:
    if listen is not None and getattr(listen, "release_group_mbid", None):
        return f"https://coverartarchive.org/release-group/{listen.release_group_mbid}/front-500"

    return settings.DEFAULT_COVER_URL


async def change_message(
    bot: Bot, message_id: int, listen: liblistenbrainz.Listen | None
):
    global old_text
    text = await get_message_text(listen)

    if text == old_text:
        return

    await bot.edit_message_media(
        media=InputMediaPhoto(
            media=await get_listen_cover_url(listen),
            caption=text,
            parse_mode=ParseMode.HTML,
        ),
        chat_id=settings.CHAT_ID,
        message_id=message_id,
    )

    old_text = text


async def init(bot: Bot) -> int:
    msg = await bot.send_photo(
        caption="Nothing is playing right now",
        photo=settings.DEFAULT_COVER_URL,
        parse_mode=ParseMode.HTML,
        chat_id=settings.CHAT_ID,
    )

    with open(PERSISTS_FILE_PATH, 'w') as f:
        data = {
            "message_id": msg.message_id
        }

        f.write(json.dumps(data))

    return msg.message_id


async def get_message_id(bot: Bot) -> int:
    if not os.path.isfile(PERSISTS_FILE_PATH):
        return await init(bot)

    with open(PERSISTS_FILE_PATH, 'r') as f:
        data = json.load(f)

    return data["message_id"]


async def main() -> None:
    bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    message_id = await get_message_id(bot)

    while True:
        await asyncio.sleep(5)

        now_playing = listen_brainz.get_playing_now(username="sakievmi")
        await change_message(bot, message_id=message_id, listen=now_playing)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
