from pydantic import BaseModel, Field
from typing import Annotated, TypedDict, Literal
import operator

class Task(BaseModel):
    id: int
    title: str
    section_type: Literal["intro", "core", "examples", "checklist", "common_mistakes", "conclusion"]
    goal: str = Field(...)
    bullets: list[str] = Field(..., min_length=3, max_length=5)
    target_words: int = Field(...)
    tags: list[str] = Field(default_factory=list)
    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False
    
class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design"] = "explainer"
    constraints: list[str] = Field(default_factory=list)
    tasks: list[Task]


class AgentState(TypedDict, total=False):
    user_prompt: str
    plan: Plan
    sections: Annotated[list[tuple[int, str]], operator.add]

    final_content: str
    file_name: str
    file_path: str
    pdf_path: str
