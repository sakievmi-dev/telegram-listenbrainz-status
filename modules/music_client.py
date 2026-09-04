from dataclasses import dataclass

import liblistenbrainz
import settings

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

    async def get_playing_now(self) -> CustomListen:
        listen = lb.get_playing_now(username=self.username)
        if listen is None:
            listen = CustomListen(listen=None, cover_url=settings.DEFAULT_COVER_URL)
            return listen

        return convert_to_custom_listen(listen)

    async def get_history(self) -> list[CustomListen]:
        history = lb.get_listens(username=self.username, count=self.history_count)
        new_history: list[CustomListen] = []

        for listen in history:
            new_history.append(convert_to_custom_listen(listen))

        return new_history
