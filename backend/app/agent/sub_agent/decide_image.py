from app.agent.state import AgentState,GlobalImagePlan,ImageSpec
from app.services.llm import llm_groq
from app.agent.prompts import DECIDE_IMAGES_SYSTEM
from langchain_core.messages import SystemMessage,HumanMessage
from app.services.state_service import update_graph_progress

def insert_placeholders(merged_md: str, images: list[ImageSpec]) -> str:
    md = merged_md
    for img in images:
        idx = md.find(img.anchor_text)
        if idx == -1:
            raise ValueError(
                f"decide_images: anchor text not found for {img.placeholder}: "
                f"{img.anchor_text!r}"
            )
        insert_at = idx + len(img.anchor_text)
        # find the next paragraph break after the anchor sentence
        next_break = md.find("\n\n", insert_at)
        insert_at = next_break if next_break != -1 else len(md)
        md = md[:insert_at] + f"\n\n{img.placeholder}" + md[insert_at:]
    return md


def decide_images(state: AgentState) -> dict:
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "image_planning", "Planning image placements...")

    planner = llm_groq.with_structured_output(GlobalImagePlan)
    merged_md = state["merged_md"]
    plan = state["plan"]
    assert plan is not None

    image_plan = planner.invoke(
        [
            SystemMessage(content=DECIDE_IMAGES_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Topic: {state['topic']}\n\n"
                    "Propose image plan (placeholders + anchor_text + prompts).\n\n"
                    f"{merged_md}"
                )
            ),
        ]
    )

    md_with_placeholders = insert_placeholders(merged_md, image_plan.images)

    return {
        "md_with_placeholders": md_with_placeholders,
        "image_specs": [img.model_dump() for img in image_plan.images],
    }