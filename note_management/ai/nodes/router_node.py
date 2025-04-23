from note_management.ai.state import State
from note_management.ai.prompt_templates.router_prompt_template import prompt_template
from llm.langchain_groq_client import groq_client

def router(state : State):
    node_destination= groq_client.invoke(
        prompt_template.format(input=state["message"])
    )
    
    #For Debugging
    print(f"Router Destination: {node_destination.content}\n\n")
    
    return {"next": node_destination.content if node_destination.content in ["chatbot", "summarizer"] else "chatbot"}