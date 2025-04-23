from typing import TypedDict, List

class State(TypedDict):
    username: str
    notes: str
    message: str
    chat_history: List[str]