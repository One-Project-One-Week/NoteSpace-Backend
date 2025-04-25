from typing import TypedDict, List

class State(TypedDict):
    username: str
    message: str
    notes: str
    summary: str
    response: str
    graph: str
    chat_history: list
    chat_history_summary: str