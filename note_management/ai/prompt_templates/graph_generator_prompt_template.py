from langchain.prompts import PromptTemplate, FewShotPromptTemplate

# # Example dataset
examples = [
    {
        "notes": """
        A simple 2-step flow:
        Step 1: User submits a form.
        Step 2: System processes the input and displays a confirmation message.
        """,
        "graph": """
        {{
            "nodes": [
                {{
                    "id": "1",
                    "type": "CustomNode",
                    "data": {{ "label": "User submits a form" }},
                    "position": {{ "x": 500, "y": 250 }}
                }},
                {{
                    "id": "2",
                    "type": "CustomNode",
                    "data": {{ "label": "System processes input and shows confirmation" }},
                    "position": {{ "x": 500, "y": 400 }}
                }}
            ],
            "edges": [
                {{
                    "id": "e1-2",
                    "source": "1",
                    "target": "2",
                    "type": "CustomEdge",
                    "data": {{ "label": "triggers" }}
                }}
            ]
        }}
        """
    },
    {
        "notes": """
        Simple login flow:
        1. User enters credentials.
        2. System checks the credentials.
        3. If valid, user is redirected to the dashboard.
        """,
        "graph": """
        {{
            "nodes": [
                {{
                    "id": "1",
                    "type": "CustomNode",
                    "data": {{ "label": "User enters credentials" }},
                    "position": {{ "x": 400, "y": 200 }}
                }},
                {{
                    "id": "2",
                    "type": "CustomNode",
                    "data": {{ "label": "System checks credentials" }},
                    "position": {{ "x": 400, "y": 350 }}
                }},
                {{
                    "id": "3",
                    "type": "CustomNode",
                    "data": {{ "label": "User redirected to dashboard" }},
                    "position": {{ "x": 400, "y": 500 }}
                }}
            ],
            "edges": [
                {{
                    "id": "e1-2",
                    "source": "1",
                    "target": "2",
                    "type": "CustomEdge",
                    "data": {{ "label": "initiates" }}
                }},
                {{
                    "id": "e2-3",
                    "source": "2",
                    "target": "3",
                    "type": "CustomEdge",
                    "data": {{ "label": "if valid" }}
                }}
            ]
        }}
        """
    }
]

# # Template for individual examples
example_prompt = PromptTemplate.from_template(
    template="Notes: {notes}\nGraph: {graph}"
)

# # System prompt (instructions for the AI)
system_prompt = """
You are a React Flow graph generator AI specialized in transforming user note summaries into node-based visualizations.

Your task is to:
- Analyze the note summary.
- Generate a JSON structure that includes:
    1. A "nodes" array representing individual entities or ideas or steps.
    2. An "edges" array representing connections between them.
- Maintain logical flow with appropriate node connections.
- Ensure the positions do not overlap unnecessarily.
- Provide only the JSON structure without any additional commentary or interpretation or markups
- DO NOT include any markdown formatting like ```json or ``` in the output
- The output should be a pure JSON string that can be parsed directly

### Node Format:
Each node must include:
- "id": A unique string identifier like "1", "2", etc.
- "type": Always "CustomNode"
- "data":  An inner object with a key "label" and a value that should be:
    * A single concept, entity, or idea (1-3 words)
    * Avoid full sentences or descriptive phrases
    * Use nouns or noun phrases
    * Keep it concise and clear
- "position": An inner object which includes "x": <number> and "y": <number> where number must be replaced with your decision of coordinate

### Edge Format:
Each edge must include:
- "id": In the format "e<source>-<target>", e.g., "e1-2"
- "source": Source node's ID
- "target": Target node's ID
- "type": "CustomEdge"
- "data": An inner object with a key "label" and a value of text representing the meaning of relationship between 2 nodes

Here are some examples:
"""

# # Few-shot prompt template
prompt_template = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=system_prompt,
    suffix="Notes: {notes}\nGraph:",
    input_variables=["notes"]
)