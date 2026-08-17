from pydantic import BaseModel, Field
from typing import Annotated, TypedDict, Literal,Optional
import operator




class ImageSpec(BaseModel):
    placeholder: str = Field(..., description="Exactly one of [[IMAGE_1]], [[IMAGE_2]], [[IMAGE_3]], in order.")
    anchor_text: str = Field(
        ...,
        description=(
            "Copy the EXACT closing sentence (verbatim, including punctuation) of the "
            "paragraph after which this image should be inserted. Must be an exact "
            "substring of the blog content provided."
        )
    )
    filename: str = Field(..., description="Just the filename with extension, no directory prefix — e.g. qkv_flow.png",)
    alt: str
    caption: str
    prompt: str = Field(..., description="Prompt to send to the image model.")
    size: Literal["1024x1024", "1024x1536", "1536x1024"] = "1024x1024"
    quality: Literal["low", "medium", "high"] = "medium"


class GlobalImagePlan(BaseModel):
    images: list[ImageSpec] = Field(default_factory=list)

                                    
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


class RouterDecision(BaseModel):
    needs_research: bool = Field(...,description="Decide whether web research is needed BEFORE planning")
    mode: Literal["closed_book", "hybrid", "open_book"]
    reason: str 
    queries: list[str] = Field(default_factory=list)
    max_results_per_query: int = Field(5)
    topic:str 


class EvidenceItem(BaseModel):
    title: str
    url: str
    content: Optional[str] = None


class EvidencePack(BaseModel):
    evidence: list[EvidenceItem] = Field(default_factory=list)

class AgentState(TypedDict, total=False):
    topic:str
    user_prompt: str
    plan: Plan
    sections: Annotated[list[tuple[int, str]], operator.add]
    queries: list[str]
    evidence: list[EvidenceItem]


    final_content: str
    file_name: str
    file_path: str
    pdf_path: str

    thread_id: str

    recency_days: int 
    mode: str
    needs_research: bool

    merged_md: str
    md_with_placeholders: str
    image_specs: list[ImageSpec]
