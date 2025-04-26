from note_management.ai.state import State
from note_management.ai.prompt_templates.chatbot_prompt_template import prompt_template
from llm.langchain_together_client import together_client
from llm.langchain_gemini_client import genai_client


def chatbot(state : State):
    
    response = genai_client.invoke(prompt_template.format(
            username=state['username'],
            chat_history_summary=state["chat_history_summary"],
            notes=state["notes"],
            question=state["message"]
        ))
    
    print(f"Chat bot response >>> {response}")
    
    return {
        "response": response
    }