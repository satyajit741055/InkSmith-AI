from app.agent.state import AgentState,GlobalImagePlan,ImageSpec
from app.services.llm import get_llm
from app.agent.prompts import DECIDE_IMAGES_SYSTEM
from langchain_core.messages import SystemMessage,HumanMessage
from app.services.state_service import update_graph_progress
import difflib

_FUZZY_THRESHOLD = 0.75

def _fuzzy_find(md: str, anchor: str) -> int:
    """Return the start index of the best fuzzy match for anchor in md, or -1."""
    words = anchor.split()
    window = len(words)
    md_words = md.split()
    best_ratio = 0.0
    best_char_idx = -1

    for i in range(len(md_words) - window + 1):
        candidate = " ".join(md_words[i : i + window])
        ratio = difflib.SequenceMatcher(None, anchor, candidate).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_char_idx = md.find(candidate)

    if best_ratio >= _FUZZY_THRESHOLD:
        print(f"insert_placeholders: fuzzy matched anchor (ratio={best_ratio:.2f}): {anchor!r}")
        return best_char_idx
    return -1


def insert_placeholders(merged_md: str, images: list[ImageSpec]) -> str:
    md = merged_md
    for img in images:
        idx = md.find(img.anchor_text)

        if idx == -1:
            idx = _fuzzy_find(md, img.anchor_text)

        if idx == -1:
            print(f"insert_placeholders: skipping {img.placeholder} — anchor not found: {img.anchor_text!r}")
            continue

        insert_at = idx + len(img.anchor_text)
        # find the next paragraph break after the anchor sentence
        next_break = md.find("\n\n", insert_at)
        insert_at = next_break if next_break != -1 else len(md)
        md = md[:insert_at] + f"\n\n{img.placeholder}" + md[insert_at:]
    return md


def decide_images(state: AgentState) -> dict:

    llm = get_llm()
    
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "image_planning", "Planning image placements...")

    planner = llm.with_structured_output(GlobalImagePlan)
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
        "image_specs": image_plan.images,  # Store ImageSpec objects directly
    }