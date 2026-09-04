import asyncio

from modules.music_client import MusicServiceClient
from modules.status_updater import NowPlayingUpdater
from modules.storage import Storage
from modules.telegram import TelegramClient

import settings

telegram_client = TelegramClient(token=settings.TOKEN, chat_id=int(settings.CHAT_ID))
music_service = MusicServiceClient(username="sakievmi")
storage = Storage()

status_updater = NowPlayingUpdater(
    telegram=telegram_client,
    music_service_client=music_service,
    storage=storage,
    text_template=settings.TEXT_TEMPLATE,
)


async def main() -> None:
    await status_updater.init()

    while True:
        await status_updater.tick()
        await asyncio.sleep(settings.POLLING_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
