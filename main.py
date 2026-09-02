import asyncio
import logging
import sys

from aiogram.types import InputMediaPhoto
import liblistenbrainz

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8900445636:AAE4Tdv4oMShYWTPd3lhiqftt32LxR9Fedo"
CHAT_ID = -1003126659685
DEFAULT_COVER_URL = "https://archive.org/download/mbid-d9d7770c-98fa-4caa-a61e-0fd0d3c6ecba/mbid-d9d7770c-98fa-4caa-a61e-0fd0d3c6ecba-35409783506_thumb500.jpg"

dispatcher = Dispatcher()
listen_brainz = liblistenbrainz.ListenBrainz()

text_template = """
Vsem privet, ya pidorBOT! Ya pokazuvayu shto slushayet STREAMER SAKIEVMI

[txthere]

Bot ezshe ne sdelan idite naxui
"""

text = ""
old_text = ""


async def get_message_text(listen: liblistenbrainz.Listen | None) -> str:
    if listen and listen.artist_name and listen.track_name:
        return text_template.replace(
            "[txthere]", f"{listen.artist_name} - {listen.track_name}"
        )

    return text_template.replace("[txthere]", "Nothing is playing right now.")


async def get_listen_cover_url(listen: liblistenbrainz.Listen | None) -> str:
    if listen is not None and getattr(listen, "release_group_mbid", None):
        return f"https://coverartarchive.org/release-group/{listen.release_group_mbid}/front-500"

    return DEFAULT_COVER_URL


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
        chat_id=CHAT_ID,
        message_id=message_id,
    )

    old_text = text


async def init(bot: Bot) -> int:
    msg = await bot.send_photo(
        caption="Nothing is playing right now",
        photo=DEFAULT_COVER_URL,
        parse_mode=ParseMode.HTML,
        chat_id=CHAT_ID,
    )

    return msg.message_id


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    message_id = await init(bot)

    while True:
        await asyncio.sleep(5)

        now_playing = listen_brainz.get_playing_now(username="sakievmi")
        await change_message(bot, message_id=message_id, listen=now_playing)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
