from pydantic import BaseModel

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