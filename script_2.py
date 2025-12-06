from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langfuse.langchain import CallbackHandler

load_dotenv()
langfuse_handler = CallbackHandler()


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash"),
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "what was the weather like in sf last week"}
        ]
    },
    config={"callbacks": [langfuse_handler]},
)

print("ALL INFORMATION")
print(response)
