from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json

# Define the output structure using Pydantic
class Node(BaseModel):
    id: str
    type: str = "CustomNode"
    data: Dict[str, str]
    position: Dict[str, int]

class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "CustomEdge"
    data: Dict[str, str]

class GraphOutput(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# Create the output parser
parser = PydanticOutputParser(pydantic_object=GraphOutput)

# Get format instructions and escape curly braces
format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

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
- Position nodes with a vertical emphasis (2:1 ratio):
    * Use x-coordinates between 500-1000
    * Use y-coordinates between 300-1000
    * Space nodes horizontally with at least 300px between them
    * Space nodes vertically with at least 200px between them
    * Center the layout horizontally (around x=500)
- Provide only the JSON structure without any additional commentary or interpretation or markups
- DO NOT include any markdown formatting like ```json or ``` in the output
- Generate nodes and suitable edges (connections) for a suitable amount (not too few or not too many) without being duplicative while avoiding overlapping positions between nodes
- The output should be a pure JSON string that can be parsed directly

{format_instructions}

### Node Format:
Each node must include:
- "id": A unique string identifier like "1", "2", etc.
- "type": Always "CustomNode"
- "data":  An inner object with a key "label" and a value that should be:
    * A single concept, entity, or idea (1-3 words)
    * Avoid full sentences or descriptive phrases
    * Use nouns or noun phrases
    * Keep it concise and clear
- "position": An inner object which includes "x": <number> and "y": <number> where:
    * x: Position horizontally (300-700)
    * y: Position vertically (100-900)
    * Ensure nodes don't overlap by maintaining minimum spacing

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
    prefix=system_prompt.format(format_instructions=format_instructions),
    suffix="Notes: {notes}\nGraph:",
    input_variables=["notes"]
)

def validate_graph_output(output: str) -> Dict[str, Any]:
    """Validate and parse the graph output."""
    try:
        # First try to parse as JSON
        json_data = json.loads(output)
        # Then validate against our Pydantic model
        validated_data = GraphOutput.model_validate_json(json_data)
        return validated_data.model_dump()
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")
    except Exception as e:
        raise ValueError(f"Invalid graph structure: {str(e)}")