from app.agent.reducer_subraph.decide_images import decide_image
from app.agent.reducer_subraph.generate_place_images import generate_and_place_images
from app.agent.reducer_subraph.merge_content import merge_content
from langgraph.graph import StateGraph,START,END
from app.agent.state import State




reducer_graph = StateGraph(State)
reducer_graph.add_node("merge_content", merge_content)
reducer_graph.add_node("decide_images", decide_image)
reducer_graph.add_node("generate_and_place_images", generate_and_place_images)



reducer_graph.add_edge(START, "merge_content")
reducer_graph.add_edge("merge_content", "decide_images")
reducer_graph.add_edge("decide_images", "generate_and_place_images")
reducer_graph.add_edge("generate_and_place_images", END)
reducer_subgraph = reducer_graph.compile()

