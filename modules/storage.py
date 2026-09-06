import json
import logging
import os
from dataclasses import dataclass

CWD = os.getcwd()
PERSISTS_FILE_PATH = CWD + "/persists.json"


@dataclass()
class State:
    message_id: int


class Storage:
    def __init__(self) -> None:
        self.state: State | None = None
        self.logging = logging.getLogger(__name__)

    def save_state(self) -> None:
        self.logging.info(f"Saving state into file {PERSISTS_FILE_PATH}")

        print(self.state)

        if self.state is None:
            self.logging.error("State is empty! Returning.")
            return

        with open(PERSISTS_FILE_PATH, "w") as f:
            data = {"message_id": self.state.message_id}
            f.write(json.dumps(data))

        self.logging.info("State was saved!")

    def load_state(self) -> None:
        self.logging.info(f"Loading state from {PERSISTS_FILE_PATH}")

        if not os.path.isfile(PERSISTS_FILE_PATH):
            self.logging.error("State file does not exist! Returning")
            return

        with open(PERSISTS_FILE_PATH, "r") as f:
            data = json.load(f)

        self.logging.info("State loaded successfully!")
        self.state = State(message_id=data["message_id"])
