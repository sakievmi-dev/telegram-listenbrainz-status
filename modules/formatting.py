import liblistenbrainz

from modules.music_client import CustomListen


def format_listen(listen: liblistenbrainz.Listen | None) -> str:
    if listen and listen.artist_name and listen.track_name:
        return f"{listen.artist_name} — {listen.track_name}"
    return "Nothing is playing right now"


class MessageBuilder:
    def __init__(self, template: str) -> None:
        self.template = template

    def replace_tag_now_playing(self, listen: CustomListen):
        self.template = self.template.replace(
            "{now_playing}", format_listen(listen.listen)
        )

    def replace_tag_listen_history(self, listen_history: list[CustomListen]):
        text_history: list[str] = []

        for listen in listen_history:
            text_history.append(f"{format_listen(listen.listen)}")

        formatted_history = "\n".join(text_history)
        self.template = self.template.replace("{listen_history}", formatted_history)
