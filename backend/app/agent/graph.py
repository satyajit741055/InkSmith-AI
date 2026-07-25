from app.agent.reducer_subraph.subgraph import reducer_subgraph
from langgraph.graph import StateGraph,START,END
from app.agent.state import State
from app.agent.nodes.orchestrator import orchestrator
from app.agent.nodes.worker import worker 
from app.agent.nodes.reducer import reducer
from app.agent.nodes.research import researcher
from langgraph.types import Send
from app.agent.nodes.router import router

def fanout(state: State):
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["title"],
                "mode": state["mode"],
                "plan": state["plan"].model_dump(),
                "evidence": state.get("evidence", []),  # Already serialized as dicts
            },
        )
        for task in state["plan"].tasks
    ]

def route(state:State):
    return "research" if State["needs_research"] else "orchestrator"

blogGraph = StateGraph(State)

blogGraph.add_node("orchestrator",orchestrator)
blogGraph.add_node("worker",worker)

blogGraph.add_node("router",router)
blogGraph.add_node("research",researcher)
blogGraph.add_node("reducer",reducer_subgraph)


blogGraph.add_edge(START,"router")
blogGraph.add_conditional_edges("router", route, ["research", "orchestrator"])
blogGraph.add_edge("research","orchestrator")
blogGraph.add_conditional_edges("orchestrator", fanout, ["worker"])
blogGraph.add_edge("worker","reducer")
blogGraph.add_edge("reducer",END)

blogGraph = blogGraph.compile()