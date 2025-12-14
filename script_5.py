import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import ToolRuntime, tool
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

langfuse_handler = CallbackHandler()

# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""


# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""

    user_id: str


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


# Set up memory
checkpointer = InMemorySaver()

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model=model,
            trigger=("tokens", 200),
            keep=("messages", 1),
        ),
    ],
)

# Run agent
# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}, "callbacks": [langfuse_handler]}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},  # Q1
    config=config,
    context=Context(user_id="1"),
)

print(response["structured_response"])  # A1

# Note that we can continue the conversation using the same `thread_id`.
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},  # Q2
    config=config,
    context=Context(user_id="1"),
)
print(response["structured_response"])  # A2

response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Do you remember my first question?"}]
    },  # Q3
    config=config,
    context=Context(user_id="1"),
)
print(response["structured_response"])  # A3
