from note_management.ai.build import app as langgraph_app
from note_management.ai.state import State

def summarize(content: str) -> str:
    try:
        response = langgraph_app.invoke({
            "username": "",
            "notes": content,
            "message": "##App_Summarizer##",
            "chat_history": []
        })
        return response['response'].content
    except Exception as err:
        print(f"Error: {err}")
        return None
        