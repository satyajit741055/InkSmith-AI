from typing import TypedDict,Annotated,Literal,Optional
from pydantic import BaseModel,Field
import operator


class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: str = ""  # keep if Tavily provides; DO NOT rely on it
    snippet: str = ""
    source: str = ""

class EvidencePack(BaseModel):
    evidence: list[EvidenceItem] = Field(default_factory=list)

class RouterDecision(BaseModel):
    needs_research : str
    mode : Literal["closed_book","hybrid","open_book"]
    queries : list[str] = Field(default_factory=list)

class Task(BaseModel):
    id: int
    title: str

    goal: str = Field(
        ...,
        description="One sentence describing what the reader should be able to do/understand after this section.",
    )
    bullets: list[str] = Field(
        ...,
        min_length=3,
        max_length=6,
        description="3–6 concrete, non-overlapping subpoints to cover in this section.",
    )
    target_words: int = Field(..., description="Target word count for this section (120–550).")

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


class State(TypedDict):
    title : str
    final : str
    plan  : Plan
    sections: Annotated[list[tuple[int, str]], operator.add]

    # router / reseach 
    mode : str
    needs_research : bool
    queries : list[str]
    evidence: list[EvidenceItem]




