from note_management.ai.state import State
from note_management.ai.prompt_templates.graph_generator_prompt_template import prompt_template
from llm.langchain_groq_client import groq_client
from llm.langchain_gemini_client import genai_client
# from llm.langchain_together_client import together_client

def graph_generator(state : State):
    
    return {
        "graph": genai_client.invoke(prompt_template.format(notes=state["summary"]))
    }