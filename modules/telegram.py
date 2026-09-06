from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InputMediaPhoto

import logging


class TelegramClient:
    def __init__(self, token: str, chat_id: int) -> None:
        self.bot = Bot(
            token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)

    async def send_initial_message(self, cover_url: str) -> int:
        logger.info("Sending initial message")

        try:
            message = await self.bot.send_photo(
                caption="",
                photo=cover_url,
                parse_mode=ParseMode.HTML,
                chat_id=self.chat_id,
            )
        except Exception as e:
            logger.error(f"Telegram API returned an error: {e}")

        logger.info("The initial message was sent")

        return message.message_id

    async def update_message(self, message_id: int, text: str, cover_url: str) -> None:
        logger.info(f"Updating message id:{message_id}")

        try:
            await self.bot.edit_message_media(
                media=InputMediaPhoto(
                    media=cover_url,
                    caption=text,
                    parse_mode=ParseMode.HTML,
                ),
                chat_id=self.chat_id,
                message_id=message_id,
            )
        except Exception as e:
            logger.error(f"Telegram API returned an error: {e}")

        logger.info(f"Message with id {message_id} was updated.")
