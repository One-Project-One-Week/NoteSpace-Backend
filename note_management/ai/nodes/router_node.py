from note_management.ai.state import State
from note_management.ai.prompt_templates.router_prompt_template import prompt_template
from llm.langchain_openrouter_client import openrouter_client
from llm.langchain_groq_client import groq_client

def router(state : State):
    res= groq_client.invoke(
        prompt_template.format(input=state["message"])
    )
    
    #For Debugging
    print(f"Router Destination: {res.content}\n\n")
    
    node_destination = res.content.strip()
    
    return {"next": node_destination if node_destination in ["chatbot", "summarizer"] else "chatbot"}