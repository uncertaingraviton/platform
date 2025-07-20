from abc import ABC, abstractmethod
from typing import Any, Dict, AsyncGenerator

class LLMBase(ABC):
    @abstractmethod
    async def chat(
        self,
        context: Dict[str, Any],
        user_input: str,
        temperature: float = 0.3,
        max_tokens: int = 512,
        stream: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Abstract chat method. Should yield response chunks if stream=True, else yield one full response.
        """
        pass 