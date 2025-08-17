from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import get_context
from llm.openai import ChatGPT4oMiniLLM
from schemas import (
    ChatRequest, ChatResponse, ProblemRequest, ProblemResponse
)
from problem_manager import ProblemManager
import asyncio
import re
import httpx

app = FastAPI(title="AI Problem Solver - Single Problem Mode")

# Allow embedding in any site (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGPT4oMiniLLM()
problem_manager = ProblemManager()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Enhanced chat endpoint that evaluates solutions against the current problem.
    """
    user_input = request.user_input.strip()
    
    # Check if user wants to see the current problem
    if any(keyword in user_input.lower() for keyword in ["show problem", "current problem", "what problem", "problem info"]):
        current_problem = problem_manager.get_active_problem_info()
        if current_problem:
            problem_info = f"🎯 Current Problem: {current_problem['title']}\n\n📝 {current_problem['description']}\n\n📊 Difficulty: {current_problem['difficulty_level']}\n🏷️ Category: {current_problem['category']}"
            return ChatResponse(
                response=problem_info,
                solution_evaluated=False
            )
        else:
            return ChatResponse(
                response="No active problem is currently set.",
                solution_evaluated=False
            )
    
    # Check if user wants to see available problems (admin function)
    if any(keyword in user_input.lower() for keyword in ["available problems", "list problems", "all problems"]):
        available_problems = problem_manager.get_available_problems()
        problem_list = "\n".join([f"- {p.title} (ID: {p.id})" for p in available_problems])
        
        return ChatResponse(
            response=f"Available problems:\n{problem_list}\n\nTo change the active problem, an admin should use the /admin/set-problem endpoint.",
            solution_evaluated=False
        )
    
    # Handle solution evaluation
    try:
        response = problem_manager.evaluate_solution(user_input)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Streaming endpoint for chat with solution evaluation.
    """
    user_input = request.user_input.strip()
    
    # Check if user wants to see the current problem
    if any(keyword in user_input.lower() for keyword in ["show problem", "current problem", "what problem", "problem info"]):
        current_problem = problem_manager.get_active_problem_info()
        if current_problem:
            problem_info = f"🎯 Current Problem: {current_problem['title']}\n\n📝 {current_problem['description']}\n\n📊 Difficulty: {current_problem['difficulty_level']}\n🏷️ Category: {current_problem['category']}"
            async def problem_stream():
                yield problem_info
            return StreamingResponse(problem_stream(), media_type="text/plain")
        else:
            async def no_problem_stream():
                yield "No active problem is currently set."
            return StreamingResponse(no_problem_stream(), media_type="text/plain")
    
    # Check if user wants to see available problems
    if any(keyword in user_input.lower() for keyword in ["available problems", "list problems", "all problems"]):
        available_problems = problem_manager.get_available_problems()
        problem_list = "\n".join([f"- {p.title} (ID: {p.id})" for p in available_problems])
        
        async def problems_stream():
            yield f"Available problems:\n{problem_list}\n\nTo change the active problem, an admin should use the /admin/set-problem endpoint."
        return StreamingResponse(problems_stream(), media_type="text/plain")
    
    # Handle solution evaluation with streaming feedback
    try:
        response = problem_manager.evaluate_solution(user_input)
        
        async def solution_stream():
            yield response.response
        
        return StreamingResponse(solution_stream(), media_type="text/plain")
        
    except Exception as e:
        async def error_stream():
            yield f"[ERROR] {str(e)}"
        return StreamingResponse(error_stream(), media_type="text/plain")

@app.get("/problem/current")
async def get_current_problem():
    """Get information about the currently active problem"""
    current_problem = problem_manager.get_active_problem_info()
    if not current_problem:
        raise HTTPException(status_code=404, detail="No active problem found")
    
    return current_problem

@app.get("/problems")
async def get_available_problems():
    """Get list of available problems (admin function)"""
    problems = problem_manager.get_available_problems()
    return {"problems": [problem.dict() for problem in problems]}

@app.post("/admin/set-problem")
async def set_active_problem(request: ProblemRequest):
    """Admin endpoint to change the active problem"""
    try:
        problem = problem_manager.set_active_problem(request.problem_id)
        return ProblemResponse(
            current_problem=problem,
            message=f"Active problem changed to: {problem.title}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-flow/config")
async def get_ai_flow_config():
    """Get AI flow configuration for the current problem"""
    current_problem = problem_manager.get_current_problem()
    if not current_problem:
        raise HTTPException(status_code=404, detail="No active problem found")
    
    return {
        "global_config": problem_manager.get_ai_flow_config(),
        "problem_specific": current_problem.ai_flow.dict() if current_problem.ai_flow else None
    } 