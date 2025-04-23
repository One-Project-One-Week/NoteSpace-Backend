from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "input": "##App_Summarizer## Can you summarize my notes from yesterday?",
        "output": "summarizer"
    },
    {
        "input": "What are my notes about?",
        "output": "chatbot"
    },
    {
        "input": "Can you summarize my notes?",
        "output": "chatbot"
    },
    {
        "input": "##App_Summarizer## Give me a summary of my meeting notes",
        "output": "summarizer"
    },
    {
        "input": "Tell me about my recent notes",
        "output": "chatbot"
    },
    {
        "input": "##App_Summarizer## Summarize my notes from last week",
        "output": "summarizer"
    }
]

example_prompt=PromptTemplate.from_template(template="Input: {input}\nOutput: {output}")

system_prompt = """
You are a routing assistant. Analyze the input and decide whether it is:
- A request that starts the specific text, ##App_Summarizer##
- A general question related to educational topics or request related to notes 

If the user asks for a summary of notes and the request message doesn't start with the specific text, ##App_Summarizer##, 
you should route respond "chatbot".

Respond with only one of the following:
    - "chatbot"
    - "summarizer"
    
Here are some examples:
"""

prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=system_prompt,
    suffix="Input: {input}\nOutput:",
)