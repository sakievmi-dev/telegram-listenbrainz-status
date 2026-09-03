import os

TOKEN: str = os.getenv("BOT_TOKEN") or ""
CHAT_ID: str = os.getenv("CHAT_ID") or ""
DEFAULT_COVER_URL = "https://archive.org/download/mbid-d9d7770c-98fa-4caa-a61e-0fd0d3c6ecba/mbid-d9d7770c-98fa-4caa-a61e-0fd0d3c6ecba-35409783506_thumb500.jpg"

# list of available tags:
# {now_playing}
TEXT_TEMPLATE = """
Это сообщение автоматизировано с помощью моего Телеграм бота. Здесь вы можете увидеть, что я слушаю в данный момент. Данные получены из моего <a href="https://listenbrainz.org/user/sakievmi/">ListenBrainz</a>.

Сейчас играет:
<b>{now_playing}</b>

Исходный код: <a href="https://github.com/sakievmi-dev/telegram-listenbrainz-status">GitHub</a>
"""
