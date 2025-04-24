from langgraph.graph import StateGraph, START, END
from .state import State
from note_management.ai.nodes.router_node import router
from note_management.ai.nodes.summarizer_node import summarizer
from note_management.ai.nodes.graph_generator_node import graph_generator

#Initialize the state graph
graph=StateGraph(State)
graph.add_node("router", router)
graph.add_node("summarizer", summarizer)
graph.add_node("graph_generator", graph_generator)

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
graph.add_edge("summarizer", "graph_generator")
graph.add_edge("graph_generator", END)
app=graph.compile()