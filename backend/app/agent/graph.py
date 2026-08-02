from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes.orchestrator import orchestrator
from app.agent.nodes.writer import writer
from app.agent.nodes.reducer import reducer
from langgraph.types import Send
import json
from pathlib import Path
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

def fanout(state:AgentState):
    return [
        Send(
            "writer",
            {
                "task": task.model_dump(),
                "plan":state["plan"].model_dump()
            },
        )
        for task in state["plan"].tasks
    ]

graph = StateGraph(AgentState)
graph.add_node("orchestrator", orchestrator)
graph.add_node("writer", writer)
graph.add_node("reducer", reducer)


graph.add_edge(START, "orchestrator")
graph.add_conditional_edges("orchestrator", fanout,["writer"])
graph.add_edge("writer", "reducer")
graph.add_edge("reducer", END)

graph = graph.compile(checkpointer=checkpointer)



if __name__ == "__main__":
    test_state = {"user_prompt": "write a blog on Future of AI in technical depth"}
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


