from note_management.ai.state import State
from note_management.ai.prompt_templates.summarizer_prompt_template import prompt_template
from llm.langchain_groq_client import groq_client_two
from llm.langchain_openrouter_client import openrouter_client
from llm.langchain_groq_client import groq_client
from llm.langchain_gemini_client import genai_client
from note_management.utils.processor.llm_input_preprocessor import tokenize_and_split_text
import re

def summarizer(state : State):
    
    chunks = tokenize_and_split_text(content=state["notes"])
    # Loop to get summarized points from notes
    summary_list = []
    for each in chunks:
        summary = groq_client.invoke(prompt_template.format(notes=each)).content
        cleaned_summary = re.sub(r"<think>.*?</think>\n?", "", summary, flags=re.DOTALL)
        summary_list.append(cleaned_summary.strip())
        
    return {
        "summary": '\n'.join(summary_list)
    }