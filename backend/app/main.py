from app.agent.graph import blogGraph
from app.agent.reducer_subraph.subgraph import reducer_subgraph


# Run graph and save state before reducer
# result = blogGraph.invoke({"title": "GPT Models"})
# print("Graph execution completed")

# To Generate Flow chart of MainGraph
# blogGraph.get_graph().draw_mermaid_png(output_file_path="graph.png")

# To Generate flow chart of SubGraph 
reducer_subgraph.get_graph().draw_mermaid_png(output_file_path="subgraph.png")


# # Save state for testing
# state_to_save = {
#     "plan": result["plan"].model_dump() if result.get("plan") else None,
#     "merged_md": result.get("merged_md", ""),
#     "md_with_placeholders": result.get("md_with_placeholders", ""),
#     "image_specs": result.get("image_specs", [])
# }

# Path("test_state.json").write_text(json.dumps(state_to_save, indent=2), encoding="utf-8")
# print("State saved to test_state.json")
