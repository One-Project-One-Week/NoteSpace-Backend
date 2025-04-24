from note_management.ai.build import app as langgraph_app
from note_management.ai.state import State

def get_summary_and_graph(content: str) -> str:
    try:
        
        response = langgraph_app.invoke({
            "notes": content,
            "message": "##App_Summarizer##",
        })
        
        return {
            "summary": response['summary'].content,
            "graph": response['graph'].content
        }
        
    except Exception as err:
        print(f"Error: {err}")
        return None
        