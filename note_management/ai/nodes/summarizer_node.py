from note_management.ai.state import State
from note_management.ai.prompt_templates.summarizer_prompt_template import prompt_template
from llm.langchain_groq_client import groq_client_two
from llm.langchain_openrouter_client import openrouter_client

def summarizer(state : State):
    
    return {
        "summary": groq_client_two.invoke(prompt_template.format(notes=state["notes"]))
    }