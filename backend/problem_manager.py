import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from schemas import (
    ProblemFramework, SolutionStep, 
    SolutionStatus, ChatResponse, AIFlowConfig
)
from problems_config import AI_FLOW_CONFIG

class ProblemManager:
    def __init__(self):
        self.problems: Dict[str, ProblemFramework] = {}
        self.current_problem: Optional[ProblemFramework] = None
        self.load_default_problems()
        # Set the first problem as active by default
        if self.problems:
            first_problem_id = list(self.problems.keys())[0]
            self.set_active_problem(first_problem_id)
    
    def load_default_problems(self):
        """Load default problem frameworks"""
        from problems_config import ALL_PROBLEMS
        
        for problem in ALL_PROBLEMS:
            self.problems[problem.id] = problem
    
    def set_active_problem(self, problem_id: str) -> ProblemFramework:
        """Set a problem as the active global problem"""
        if problem_id not in self.problems:
            raise ValueError(f"Problem {problem_id} not found")
        
        self.current_problem = self.problems[problem_id]
        return self.current_problem
    
    def get_current_problem(self) -> Optional[ProblemFramework]:
        """Get the currently active problem"""
        return self.current_problem
    
    def evaluate_solution(self, user_input: str) -> ChatResponse:
        """Evaluate a user's proposed solution step against the current problem"""
        if not self.current_problem:
            return ChatResponse(
                response="No active problem set. Please contact an administrator.",
                solution_evaluated=False
            )
        
        # For now, we'll evaluate against the first step
        # In a real system, you might want to determine which step the user is addressing
        reference_step = self.current_problem.reference_steps[0]
        
        # Evaluate the solution using AI logic with flow configuration
        evaluation_result = self._evaluate_step_logic(user_input, reference_step)
        
        # Generate response with AI flow suggestions
        response = ChatResponse(
            response=evaluation_result["feedback"],
            solution_evaluated=True
        )
        
        return response
    
    def _evaluate_step_logic(self, user_input: str, reference_step: str) -> Dict[str, any]:
        """Evaluate a solution step using logic and reference framework with AI flow"""
        user_input_lower = user_input.lower()
        
        # Check if user input contains relevant keywords from reference step
        relevant_keywords = self._extract_keywords(reference_step)
        keyword_matches = sum(1 for keyword in relevant_keywords if keyword in user_input_lower)
        
        # Get AI flow configuration for current problem
        ai_flow = self.current_problem.ai_flow if self.current_problem else None
        
        if keyword_matches >= len(relevant_keywords) * 0.6:  # 60% keyword match threshold
            status = SolutionStatus.APPROVED
            if ai_flow and ai_flow.suggestions:
                # Use AI flow suggestions for positive feedback
                suggestion = self._get_random_suggestion(ai_flow.suggestions)
                feedback = f"Good solution! Your approach addresses the key elements: {reference_step}\n\n💡 Suggestion: {suggestion}"
            else:
                feedback = f"Good solution! Your approach addresses the key elements: {reference_step}"
                
        elif keyword_matches >= len(relevant_keywords) * 0.3:  # 30% keyword match threshold
            status = SolutionStatus.NEEDS_REFINEMENT
            if ai_flow and ai_flow.hints:
                # Use AI flow hints for guidance
                hint = self._get_random_suggestion(ai_flow.hints)
                feedback = f"Your solution is on the right track but could be more comprehensive. Consider: {reference_step}\n\n💡 Hint: {hint}"
            else:
                feedback = f"Your solution is on the right track but could be more comprehensive. Consider: {reference_step}"
        else:
            status = SolutionStatus.REJECTED
            if ai_flow and ai_flow.hints:
                # Use AI flow hints for guidance
                hint = self._get_random_suggestion(ai_flow.hints)
                feedback = f"Your solution doesn't seem to address the expected approach: {reference_step}\n\n💡 Hint: {hint}"
            else:
                feedback = f"Your solution doesn't seem to address the expected approach: {reference_step}"
        
        return {
            "status": status,
            "feedback": feedback
        }
    
    def _get_random_suggestion(self, suggestions: List[str]) -> str:
        """Get a random suggestion from the list"""
        import random
        return random.choice(suggestions) if suggestions else ""
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from reference text"""
        # Simple keyword extraction - in production, use NLP libraries
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words = text.lower().split()
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return keywords[:5]  # Top 5 keywords
    
    def get_available_problems(self) -> List[ProblemFramework]:
        """Get list of available problems for admin selection"""
        return list(self.problems.values())
    
    def get_active_problem_info(self) -> Optional[Dict]:
        """Get information about the currently active problem"""
        if not self.current_problem:
            return None
        
        return {
            "id": self.current_problem.id,
            "title": self.current_problem.title,
            "description": self.current_problem.description,
            "difficulty_level": self.current_problem.difficulty_level,
            "category": self.current_problem.category,
            "total_steps": self.current_problem.required_steps
        }
    
    def get_ai_flow_config(self) -> Dict:
        """Get the global AI flow configuration"""
        return AI_FLOW_CONFIG
