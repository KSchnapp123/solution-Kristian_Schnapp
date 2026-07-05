from pydantic import BaseModel
from typing import Optional

class TodoResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: str

class TodoResponseId(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: str
    completed: bool
    user_id: int

class TodoBody(BaseModel):
    todo: str
    completed: bool
    userId: int


class TodoPatch(BaseModel):
    todo: Optional[str] = None
    completed: Optional[bool] = None
    userId: Optional[int] = None