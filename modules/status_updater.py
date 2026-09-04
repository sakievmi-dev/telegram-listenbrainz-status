from modules.formatting import MessageBuilder
from modules.music_client import CustomListen, MusicServiceClient
from modules.storage import Storage, State
from modules.telegram import TelegramClient
import settings


class NowPlayingUpdater:
    def __init__(
        self,
        telegram: TelegramClient,
        music_service_client: MusicServiceClient,
        storage: Storage,
        text_template: str,
    ) -> None:
        self._telegram: TelegramClient = telegram
        self._music_service: MusicServiceClient = music_service_client
        self._storage: Storage = storage
        self._message_id: int
        self._text_template: str = text_template
        self._last_text: str | None = None

    async def tick(self):
        now_playing: CustomListen = await self._music_service.get_playing_now()

        message_builder = MessageBuilder(template=self._text_template)
        message_builder.replace_tag_now_playing(now_playing)
        message_builder.replace_tag_listen_history(
            await self._music_service.get_history()
        )

        if self._last_text == message_builder.template:
            return

        await self._telegram.update_message(
            message_id=self._message_id,
            text=message_builder.template,
            cover_url=now_playing.cover_url,
        )

        self._last_text = message_builder.template

    async def init(self):
        self._storage.load_state()
        state = self._storage.state

        if state is None:
            message_id = await self._telegram.send_initial_message(
                cover_url=settings.DEFAULT_COVER_URL
            )

            new_state: State = State(message_id=message_id)
            self._storage.state = new_state
            state = new_state

            self._storage.save_state()

        self._message_id = state.message_id
