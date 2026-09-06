from dataclasses import dataclass

import liblistenbrainz
import settings
import logging

lb = liblistenbrainz.ListenBrainz()


@dataclass()
class CustomListen:
    listen: liblistenbrainz.Listen | None
    cover_url: str


def convert_to_custom_listen(listen: liblistenbrainz.Listen) -> CustomListen:
    cover_url = settings.DEFAULT_COVER_URL
    if getattr(listen, "release_group_mbid", None):
        cover_url = f"https://coverartarchive.org/release-group/{listen.release_group_mbid}/front-500"

    return CustomListen(listen, cover_url)


class MusicServiceClient:
    def __init__(self, username: str, history_count: int = 5):
        self.username: str = username
        self.history_count: int = history_count
        self.logging = logging.getLogger(__name__)

    async def get_playing_now(self) -> CustomListen:
        self.logging.info(f"Getting 'playing now' listen from {self.username}")

        try:
            listen = lb.get_playing_now(username=self.username)
            if listen is not None:
                self.logging.info("ListenBrainz returned None")
                return convert_to_custom_listen(listen)
        except Exception as e:
            self.logging.error(f"ListenBrainz returned an error: {e}. Returning None.")

        listen = CustomListen(listen=None, cover_url=settings.DEFAULT_COVER_URL)
        return listen

    async def get_history(self) -> list[CustomListen]:
        self.logging.info(
            f"Getting recent listens ({self.history_count} latest) from {self.username}"
        )

        new_history: list[CustomListen] = []

        try:
            history = lb.get_listens(username=self.username, count=self.history_count)

            for listen in history:
                new_history.append(convert_to_custom_listen(listen))
        except:
            self.logging.error("An error occured when creating recent listens list.")

        return new_history
