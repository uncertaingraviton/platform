import os
import httpx
import asyncio
from typing import Any, Dict, AsyncGenerator
from .base import LLMBase

# Placeholder for Gemini API key (replace with real key in production)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Update if needed

class GeminiLLM(LLMBase):
    async def chat(
        self,
        context: Dict[str, Any],
        user_input: str,
        temperature: float = 0.3,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Calls Gemini 2.0 Flash API with the merged context and user input.
        Yields response chunks if stream=True, else yields one full response.
        """
        # Format prompt as required by Gemini API
        prompt_parts = []
        for role in context.get("roles", []):
            for k, v in role.items():
                prompt_parts.append({"role": k, "parts": [v]})
        prompt_parts.append({"role": "user", "parts": [user_input]})

        payload = {
            "contents": prompt_parts,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
            "stream": stream,
        }

        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=10.0) as client:
            if stream:
                async with client.stream("POST", GEMINI_API_URL, json=payload, headers=headers) as response:
                    async for line in response.aiter_lines():
                        if line.strip():
                            # Parse and yield chunk
                            try:
                                data = httpx.Response(200, content=line).json()
                                chunk = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                                if chunk:
                                    yield chunk
                            except Exception:
                                continue
            else:
                resp = await client.post(GEMINI_API_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                yield text 