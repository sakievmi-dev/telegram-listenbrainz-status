from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto


class TelegramClient:
    def __init__(self, token: str, chat_id: int) -> None:
        self.bot = Bot(
            token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.chat_id = chat_id

    async def send_initial_message(self, cover_url: str) -> int:
        message = await self.bot.send_photo(
            caption="",
            photo=cover_url,
            parse_mode=ParseMode.HTML,
            chat_id=self.chat_id,
        )

        return message.message_id

    async def update_message(self, message_id: int, text: str, cover_url: str) -> None:
        await self.bot.edit_message_media(
            media=InputMediaPhoto(
                media=cover_url,
                caption=text,
                parse_mode=ParseMode.HTML,
            ),
            chat_id=self.chat_id,
            message_id=message_id,
        )
