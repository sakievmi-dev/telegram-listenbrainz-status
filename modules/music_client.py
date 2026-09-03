from dataclasses import dataclass

import liblistenbrainz
import settings

lb = liblistenbrainz.ListenBrainz()


@dataclass()
class CustomListen:
    listen: liblistenbrainz.Listen
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

        # TODO: make listen history
        self.history = []

    async def get_playing_now(self) -> CustomListen | None:
        listen = lb.get_playing_now(username=self.username)
        if listen is None:
            return None

        return convert_to_custom_listen(listen)
