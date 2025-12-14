import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langchain_openai import ChatOpenAI
from langfuse.langchain import CallbackHandler

load_dotenv()

# Initialize components
langfuse_handler = CallbackHandler()

# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.

After you retrieve the weather information, provide a friendly response to the user."""


# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""

    user_id: str = "2"  # Default user_id


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

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
)
