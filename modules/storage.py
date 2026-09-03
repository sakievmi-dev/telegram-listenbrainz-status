import json
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

    def save_state(self) -> None:
        print(self.state)

        if self.state is None:
            return

        with open(PERSISTS_FILE_PATH, "w") as f:
            data = {"message_id": self.state.message_id}
            f.write(json.dumps(data))

    def load_state(self) -> None:
        if not os.path.isfile(PERSISTS_FILE_PATH):
            return

        with open(PERSISTS_FILE_PATH, "r") as f:
            data = json.load(f)
        self.state = State(message_id=data["message_id"])
