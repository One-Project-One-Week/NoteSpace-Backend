from note_management.ai.state import State
from note_management.ai.prompt_templates.router_prompt_template import prompt_template
from llm.langchain_openrouter_client import openrouter_client
from llm.langchain_groq_client import groq_client

def router(state : State):
    
    if state["message"] == "##App_Summarizer##":
        node_destination = "summarizer"
    else:
        node_destination = "chatbot"
    
    #For Debugging
    print(f"Router Destination: {node_destination}\n\n")
    
    return {"next": node_destination if node_destination in ["chatbot", "summarizer"] else "chatbot"}