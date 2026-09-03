import liblistenbrainz


def format_listen(listen: liblistenbrainz.Listen | None) -> str:
    if listen and listen.artist_name and listen.track_name:
        return f"{listen.artist_name} — {listen.track_name}"
    return "Nothing is playing right now"


class MessageBuilder:
    def __init__(self, template: str) -> None:
        self.template = template

    def replace_tag_now_playing(self, listen: liblistenbrainz.Listen):
        self.template = self.template.replace("{now_playing}", format_listen(listen))
