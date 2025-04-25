from note_management.ai.build import app as langgraph_app
from note_management.ai.state import State

def use_chatbot(username: str, message: str, chat_history: list, notes: str) -> str:
    response = langgraph_app.invoke({
        "username": username,
        "chat_history": chat_history,
        "message": message,
        "notes": notes
    })
    
    return {
        "response": response['response'].content,
    }
        