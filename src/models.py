from pydantic import BaseModel, Field
from typing import Optional

class Note(BaseModel):
    id: str = Field(..., description="Unique identifier for the note")
    title: str = Field(..., max_length=100, description="Title of the note")
    content: str = Field(..., description="Content of the note")
    owner_id: Optional[str] = Field(None, description="ID of the user who owns the note")

class User(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., max_length=50, description="Username")
    email: str = Field(..., description="User email")

# Additional models like Response schemas can be added here
