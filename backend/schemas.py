from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    user_input: str = Field(..., description="User's freeform thought or question.")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant's reply.")
    out_of_scope: Optional[bool] = Field(False, description="True if the user input was out of context.") 