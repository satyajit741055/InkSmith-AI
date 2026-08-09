from langgraph.graph import StateGraph,START,END
from app.agent.state import AgentState
from app.agent.sub_agent.merger import merge_content
from app.agent.sub_agent.decide_image import decide_images
from app.agent.sub_agent.generate_image import generate_and_place_images


sub_graph = StateGraph(AgentState)
sub_graph.add_node("merger",merge_content)
sub_graph.add_node("decide_image",decide_images)
sub_graph.add_node("generate_and_place_images",generate_and_place_images)


sub_graph.add_edge(START,"merger")
sub_graph.add_edge("merger","decide_image")
# sub_graph.add_edge("decide_image",END)
sub_graph.add_edge("decide_image","generate_and_place_images")
sub_graph.add_edge("generate_and_place_images",END)

sub_agent = sub_graph.compile()