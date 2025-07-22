from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_context
from backend.llm.openai import ChatGPT4oMiniLLM
from backend.schemas import ChatRequest, ChatResponse
import asyncio
import re

app = FastAPI(title="Reasoning Chatbot (ChatGPT-4o Mini)")

# Allow embedding in any site (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGPT4oMiniLLM()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Accepts user input, merges with daily context, and returns ChatGPT-4o Mini response.
    Stateless: does not store user data.
    """
    context = get_context()
    user_input = request.user_input.strip()
    topic = str(context.get("roles", [{}])[0].get("system", "")).lower()
    topic_value = topic.split("Topic:")[-1:].pop().split("•")[0].replace('"', '').strip() if "Topic:" in topic else ""
    if "out-of-scope" in topic:
        if topic_value == "greetings":
            greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "yo", "sup", "what's up", "howdy"]
            if not any(greet in user_input.lower() for greet in greetings):
                return ChatResponse(response="Out of scope. Please ask about today's topic only.", out_of_scope=True)
        else:
            if topic_value and topic_value not in user_input.lower():
                return ChatResponse(response="Out of scope. Please ask about today's topic only.", out_of_scope=True)
    # Call ChatGPT-4o Mini (non-streaming)
    try:
        chunks = []
        async for chunk in llm.chat(context, user_input, stream=False):
            chunks.append(chunk)
        return ChatResponse(response="".join(chunks))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Streaming endpoint for chat (yields response chunks).
    """
    context = get_context()
    user_input = request.user_input.strip()
    topic = str(context.get("roles", [{}])[0].get("system", "")).lower()
    topic_value = topic.split("Topic:")[-1:].pop().split("•")[0].replace('"', '').strip() if "Topic:" in topic else ""
    async def event_stream():
        try:
            if "out-of-scope" in topic:
                if topic_value == "greetings":
                    greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening", "yo", "sup", "what's up", "howdy"]
                    if not any(greet in user_input.lower() for greet in greetings):
                        yield "Out of scope. Please ask about today's topic only."
                        return
                else:
                    if topic_value and topic_value not in user_input.lower():
                        yield "Out of scope. Please ask about today's topic only."
                        return
            async for chunk in llm.chat(context, user_input, stream=True):
                yield chunk
        except Exception as e:
            yield f"[ERROR] {str(e)}"
    return StreamingResponse(event_stream(), media_type="text/plain") 