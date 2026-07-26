
from app.agent.state import State
from app.agent.llm import llm
from app.agent.state import GlobalImagePlan
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import DECIDE_IMAGES_SYSTEM
import logfire


def decide_image(state:State)->dict:
    planner = llm.with_structured_output(GlobalImagePlan)
    merged_md = state["merged_md"]
    plan = state["plan"]
    assert plan is not None 
    with logfire.span("Deciding images"):
        image_plan = planner.invoke(
            [
                SystemMessage(content=DECIDE_IMAGES_SYSTEM),
                HumanMessage(
                    content=(
                        f"Blog kind: {plan.blog_kind}\n"
                        f"Topic: {state['title']}\n\n"
                        "Insert placeholders + propose image prompts.\n\n"
                        f"{merged_md}"
                    )
                ),
            ]
        )

        logfire.info("Images decided", image_count=len(image_plan.images), image_specs=[img.model_dump() for img in image_plan.images])
  
        return {
            "md_with_placeholders": image_plan.md_with_placeholders,
            "image_specs": [img.model_dump() for img in image_plan.images],
        }

