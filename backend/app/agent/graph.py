from langgraph.graph import StateGraph,START,END
from app.agent.state import State
from app.agent.nodes.orchestrator import orchestrator
from app.agent.nodes.worker import worker 
from app.agent.nodes.reducer import reducer
from langgraph.types import Send

def fanout(state:State):
    return [Send("worker", {"task": task, "topic":state["title"] , "plan":state["plan"]}) for task in state["plan"].tasks]

blogGraph = StateGraph(State)

blogGraph.add_node("orchestrator",orchestrator)
blogGraph.add_node("worker",worker)
blogGraph.add_node("reducer",reducer)


blogGraph.add_edge(START,"orchestrator")
blogGraph.add_conditional_edges("orchestrator", fanout, ["worker"])
blogGraph.add_edge("worker","reducer")
blogGraph.add_edge("reducer",END)

blogGraph = blogGraph.compile()