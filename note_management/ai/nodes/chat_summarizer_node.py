from note_management.ai.state import State
from note_management.ai.prompt_templates.chatbot_prompt_template import prompt_template
from note_management.utils.summarizer.chat_summarizer import summarize_chat

def chat_summariser(state : State):
    
    if len(state["chat_history"]) < 2:
        print(f"No chat history, {state['chat_history']}")
        return {"chat_history_summary": "No Chat History"}
    
    print(state["chat_history"])
    summary = summarize_chat(content=state["chat_history"])
    
    print(f"chat history >>> {summary}")
    
    return {
        "chat_history_summary": summary
    }