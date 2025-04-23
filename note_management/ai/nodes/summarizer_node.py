from note_management.ai.state import State
from note_management.ai.prompt_templates.summarizer_prompt_template import prompt_template
from llm.langchain_groq_client import groq_client

def summarizer(state : State):
    summary = groq_client.invoke(
        prompt_template.format(notes=state.notes)
    )
    
    return {
        "response": summary
    }