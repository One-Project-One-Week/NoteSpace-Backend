from langgraph.graph import StateGraph, START, END
from .state import State
from note_management.ai.nodes.router_node import router
from note_management.ai.nodes.summarizer_node import summarizer

#Initialize the state graph
graph=StateGraph(State)
graph.add_node("router", router)
graph.add_node("summarizer", summarizer)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    lambda res : res["next"],
    {
        "chatbot": "summarizer",
        "summarizer": "summarizer"
    }
)
# graph.add_edge("chatbot", END)
graph.add_edge("summarizer", END)
app=graph.compile()