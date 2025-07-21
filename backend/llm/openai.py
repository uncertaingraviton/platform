import os
from dotenv import load_dotenv
import httpx
from typing import Any, Dict, AsyncGenerator
from .base import LLMBase

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set.")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o"

class ChatGPT4oMiniLLM(LLMBase):
    async def chat(
        self,
        context: Dict[str, Any],
        user_input: str,
        temperature: float = 0.3,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Calls OpenAI ChatGPT-4o Mini API with the merged context and user input.
        Yields response chunks if stream=True, else yields one full response.
        """
        messages = []
        for role in context.get("roles", []):
            for k, v in role.items():
                if k == "system":
                    messages.append({"role": "system", "content": v})
                elif k == "assistant":
                    messages.append({"role": "assistant", "content": v})
        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=20.0) as client:
            if stream:
                async with client.stream("POST", OPENAI_API_URL, json=payload, headers=headers) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[len("data: "):].strip()
                            if data == "[DONE]":
                                break
                            try:
                                chunk = httpx.Response(200, content=data).json()
                                delta = chunk["choices"][0]["delta"].get("content", "")
                                if delta:
                                    yield delta
                            except Exception:
                                continue
            else:
                resp = await client.post(OPENAI_API_URL, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                yield text 