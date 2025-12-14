import os
from contextlib import asynccontextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import create_agent

# from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import ToolRuntime, tool
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel

load_dotenv()

# Initialize components
langfuse_handler = CallbackHandler()

# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""

    user_id: str  # Default user_id


# Define tools
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


# Configure model
model = ChatOpenAI(
    model="gpt-4o",
    base_url=os.getenv("LLM_API_URL"),
    api_key="",
    default_headers={"Authorization": os.getenv("LLM_API_TOKEN")},
)


# Define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""

    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


# Set up in-memory checkpointer for FastAPI sample server
checkpointer = InMemorySaver()

# The platform handles persistence automatically
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer,
    # middleware=[
    #     SummarizationMiddleware(
    #         model=model,
    #         trigger=("tokens", 200),
    #         keep=("messages", 1),
    #     ),
    # ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("Agent server starting...")
    yield
    print("Agent server shutting down...")


app = FastAPI(title="LangChain Agent API", lifespan=lifespan)

# Enable CORS for Agent Chat UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class AgentInput(BaseModel):
    messages: list[Message]
    user_id: str
    thread_id: str = "default"  # Default thread ID for conversation tracking


class AgentResponse(BaseModel):
    messages: list


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/invoke")
async def invoke_agent(input_data: AgentInput):
    """Invoke the agent with a user message."""
    messages = [
        {"role": msg.role, "content": msg.content} for msg in input_data.messages
    ]

    # Configure the agent with thread_id for conversation memory
    config = {
        "configurable": {"thread_id": input_data.thread_id},
        "callbacks": [langfuse_handler],
    }

    # Invoke the agent with context
    result = agent.invoke(
        {"messages": messages},
        config=config,
        context=Context(user_id=input_data.user_id),
    )

    return {"response": result}
