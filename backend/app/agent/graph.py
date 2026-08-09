from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes.orchestrator import orchestrator
from app.agent.nodes.writer import writer
from app.agent.nodes.reducer import reducer
from app.agent.nodes.router import router
from app.agent.nodes.research import research
from langgraph.types import Send
import json
from pathlib import Path
from langgraph.checkpoint.memory import MemorySaver
from app.agent.sub_agent.sub_graph import sub_agent

checkpointer = MemorySaver()

def fanout(state:AgentState):
    total_tasks = len(state["plan"].tasks)
    return [
        Send(
            "writer",
            {
                "task": task.model_dump(),
                "plan": state["plan"].model_dump(),
                "thread_id": state.get("thread_id"),
                "total_tasks": total_tasks,
                "topic":state["topic"],
                "mode":state["mode"],
                "recency_days": state["recency_days"],
                "evidence": [e.model_dump() for e in state.get("evidence", [])],
            },
        )
        for task in state["plan"].tasks
    ]


def route_next(state: AgentState) -> str:
    return "research" if state["needs_research"] else "orchestrator"


graph = StateGraph(AgentState)
graph.add_node("router",router)
graph.add_node("research",research)
graph.add_node("orchestrator", orchestrator)
graph.add_node("writer", writer)
graph.add_node("reducer", reducer)
graph.add_node("sub_agent",sub_agent)


graph.add_edge(START, "router")
graph.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
graph.add_edge("research", "orchestrator")
graph.add_conditional_edges("orchestrator", fanout,["writer"])
graph.add_edge("writer", "sub_agent")

graph = graph.compile(checkpointer=checkpointer)



if __name__ == "__main__":
    test_state = {"user_prompt": "write a blog Python Basics for Beginners"}
    config = {"configurable": {"thread_id": "thread-1"}}

    result = graph.invoke(test_state, config)
    state_snapshot = graph.get_state(config)
    values = state_snapshot.values
    serializable = {
        **values,
        "plan": values["plan"].model_dump() if hasattr(values.get("plan"), "model_dump") else values.get("plan"),
    }
    
    output_path = Path("output/state_snapshot.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2)


