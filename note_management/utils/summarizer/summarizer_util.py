from note_management.ai.build import app as langgraph_app

def get_summary_and_graph(content: str):
    response = langgraph_app.invoke({
        "notes": content,
        "message": "##App_Summarizer##",
    })
    
    return {
        "summary": response['summary'],
        "graph": response['graph']
    }
        