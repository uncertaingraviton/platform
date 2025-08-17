from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

class SolutionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REFINEMENT = "needs_refinement"

class SolutionStep(BaseModel):
    id: str
    user_input: str
    proposed_solution: str
    status: SolutionStatus
    feedback: Optional[str] = None
    timestamp: datetime
    step_number: int

class AIFlowConfig(BaseModel):
    evaluation_criteria: List[str]
    suggestions: List[str]
    hints: List[str]

class ProblemFramework(BaseModel):
    id: str
    title: str
    description: str
    reference_steps: List[str]
    required_steps: int
    difficulty_level: str
    category: str
    ai_flow: Optional[AIFlowConfig] = None

class ChatRequest(BaseModel):
    user_input: str = Field(..., description="User's proposed solution or question")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant's evaluation and feedback")
    out_of_scope: Optional[bool] = Field(False, description="True if the user input was out of context")
    solution_evaluated: bool = Field(False, description="Whether the input was evaluated as a solution")

class ProblemRequest(BaseModel):
    problem_id: str = Field(..., description="ID of the problem to set as active")

class ProblemResponse(BaseModel):
    current_problem: Optional[ProblemFramework] = Field(None, description="Currently active problem")
    message: str = Field(..., description="Response message") 