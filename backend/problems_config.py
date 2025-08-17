"""
Configuration file for problem frameworks.
Add new problems here to make them available in the system.
"""

from schemas import ProblemFramework

# AI Flow and Suggestions Configuration
AI_FLOW_CONFIG = {
    "evaluation_prompts": {
        "initial_assessment": "Analyze the user's solution step and provide constructive feedback.",
        "detailed_feedback": "Provide specific suggestions for improvement based on the reference framework.",
        "encouragement": "Acknowledge progress and encourage continued effort."
    },
    "suggestion_types": {
        "hint": "Provide a subtle hint without giving away the complete answer",
        "clarification": "Ask clarifying questions to better understand the user's approach",
        "alternative_approach": "Suggest alternative methods or perspectives",
        "next_step": "Guide the user toward the next logical step"
    },
    "response_templates": {
        "positive": "Great work! Your approach shows good understanding of {concept}.",
        "needs_improvement": "You're on the right track. Consider focusing on {specific_area}.",
        "encouragement": "Keep going! You're making progress toward the solution."
    }
}

# Default problem frameworks
DEFAULT_PROBLEMS = [
    ProblemFramework(
        id="math_sequence",
        title="Mathematical Sequence Problem",
        description="Find the next number in the sequence: 2, 4, 8, 16, ?",
        reference_steps=[
            "Identify the pattern in the sequence",
            "Recognize it's a geometric sequence",
            "Calculate the common ratio",
            "Apply the pattern to find the next term",
            "Verify the solution fits the pattern"
        ],
        required_steps=5,
        difficulty_level="intermediate",
        category="mathematics",
        # AI Flow Configuration
        ai_flow={
            "evaluation_criteria": [
                "Pattern recognition accuracy",
                "Mathematical reasoning clarity",
                "Solution verification approach"
            ],
            "suggestions": [
                "Look for relationships between consecutive terms",
                "Consider if the pattern involves multiplication or addition",
                "Test your solution by applying the pattern backwards"
            ],
            "hints": [
                "What operation transforms 2 to 4?",
                "Is this pattern consistent throughout the sequence?",
                "How can you verify your answer is correct?"
            ]
        }
    ),
    ProblemFramework(
        id="business_strategy",
        title="Business Strategy Development",
        description="Develop a strategy for a new product launch in a competitive market",
        reference_steps=[
            "Conduct market research and analysis",
            "Identify target audience and positioning",
            "Analyze competitive landscape",
            "Develop unique value proposition",
            "Create marketing and launch plan",
            "Define success metrics and KPIs"
        ],
        required_steps=6,
        difficulty_level="advanced",
        category="business",
        # AI Flow Configuration
        ai_flow={
            "evaluation_criteria": [
                "Market analysis depth",
                "Strategic thinking quality",
                "Practical implementation feasibility"
            ],
            "suggestions": [
                "Consider both quantitative and qualitative market data",
                "Focus on unique differentiators from competitors",
                "Ensure your strategy is measurable and actionable"
            ],
            "hints": [
                "What makes your product different from existing solutions?",
                "How will you measure the success of your strategy?",
                "What are the biggest risks to your launch plan?"
            ]
        }
    ),
    ProblemFramework(
        id="coding_algorithm",
        title="Algorithm Design Challenge",
        description="Design an efficient algorithm to find the longest common subsequence",
        reference_steps=[
            "Understand the problem requirements",
            "Identify input constraints and edge cases",
            "Design a brute force approach first",
            "Optimize using dynamic programming",
            "Analyze time and space complexity",
            "Test with various test cases"
        ],
        required_steps=6,
        difficulty_level="advanced",
        category="programming",
        # AI Flow Configuration
        ai_flow={
            "evaluation_criteria": [
                "Problem understanding completeness",
                "Algorithm design efficiency",
                "Complexity analysis accuracy"
            ],
            "suggestions": [
                "Start with a simple example to understand the pattern",
                "Consider how overlapping subproblems can be optimized",
                "Think about edge cases like empty strings or single characters"
            ],
            "hints": [
                "What happens when you have overlapping subproblems?",
                "How can you build the solution from smaller subproblems?",
                "What's the relationship between the current cell and previous cells?"
            ]
        }
    ),
    ProblemFramework(
        id="creative_writing",
        title="Creative Story Development",
        description="Create a compelling short story with a twist ending",
        reference_steps=[
            "Develop a unique premise or concept",
            "Create well-defined characters with clear motivations",
            "Establish the setting and atmosphere",
            "Build tension and conflict throughout the story",
            "Craft a surprising but logical twist ending",
            "Revise for clarity and impact"
        ],
        required_steps=6,
        difficulty_level="intermediate",
        category="creative",
        # AI Flow Configuration
        ai_flow={
            "evaluation_criteria": [
                "Creativity and originality",
                "Character development depth",
                "Narrative structure effectiveness"
            ],
            "suggestions": [
                "Show character motivations through actions, not just descriptions",
                "Use sensory details to create immersive settings",
                "Plant subtle clues for the twist throughout the story"
            ],
            "hints": [
                "What does your character want most? What's stopping them?",
                "How can you make the twist both surprising and inevitable?",
                "What details can you add to make the setting more vivid?"
            ]
        }
    ),
    ProblemFramework(
        id="scientific_method",
        title="Scientific Experiment Design",
        description="Design an experiment to test a hypothesis about plant growth",
        reference_steps=[
            "Formulate a clear, testable hypothesis",
            "Identify independent and dependent variables",
            "Design control and experimental groups",
            "Plan data collection methods and timeline",
            "Consider potential confounding factors",
            "Outline expected results and analysis methods"
        ],
        required_steps=6,
        difficulty_level="intermediate",
        category="science",
        # AI Flow Configuration
        ai_flow={
            "evaluation_criteria": [
                "Hypothesis clarity and testability",
                "Experimental design rigor",
                "Control of variables effectiveness"
            ],
            "suggestions": [
                "Ensure your hypothesis is specific and measurable",
                "Include multiple control groups for better comparison",
                "Consider environmental factors that might affect results"
            ],
            "hints": [
                "What exactly are you changing between groups?",
                "How will you measure the effect of your independent variable?",
                "What other factors might influence your results?"
            ]
        }
    )
]

# Add your custom problems here
CUSTOM_PROBLEMS = [
    # Example custom problem:
    # ProblemFramework(
    #     id="your_problem_id",
    #     title="Your Problem Title",
    #     description="Description of your problem",
    #     reference_steps=[
    #         "Step 1 description",
    #         "Step 2 description",
    #         "Step 3 description"
    #     ],
    #     required_steps=3,
    #     difficulty_level="beginner",  # beginner, intermediate, advanced
    #     category="your_category",
    #     # AI Flow Configuration
    #     ai_flow={
    #         "evaluation_criteria": [
    #             "Criterion 1",
    #             "Criterion 2"
    #         ],
    #         "suggestions": [
    #             "Suggestion 1",
    #             "Suggestion 2"
    #         ],
    #         "hints": [
    #             "Hint 1",
    #             "Hint 2"
    #         ]
    #     }
    # )
]

# Combine default and custom problems
ALL_PROBLEMS = DEFAULT_PROBLEMS + CUSTOM_PROBLEMS
