from typing import TypedDict, List

class State(TypedDict):
    username: str
    notes: str
    message: str
    chat_history: list
    response: str
    graph_data: list