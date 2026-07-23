from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import operator

class Task(BaseModel):
    id : int 
    title : str
    brief : str = Field(...,description="What to cover in details")

class Plan(BaseModel):
    blog_title : str
    tasks : list[Task]

class State(TypedDict):
    title : str
    final : str
    plan  : Plan
    sections : Annotated[list[str],operator.add]



