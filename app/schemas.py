from pydantic import BaseModel
from typing import Dict, Any

class ProjectRequest(BaseModel):
    user_request: str

class ProjectResponse(BaseModel):
    id: int
    title: str
    user_request: str
    plan_data: Dict[str, Any]

    class Config:
        from_attributes = True