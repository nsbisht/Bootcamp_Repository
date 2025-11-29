# Import required libraries
from dotenv import load_dotenv  # For loading environment variables from .env file
from langfuse.langchain import (
    CallbackHandler,
)  # For tracing and monitoring LangChain calls
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)  # Google's Gemini model integration
from langchain_core.prompts import ChatPromptTemplate  # For creating structured prompts

# Load environment variables from .env file (API keys, credentials, etc.)
load_dotenv()

# Initialize Langfuse callback handler for tracing and observability
# This tracks all LLM calls, prompts, and responses for monitoring and debugging
langfuse_handler = CallbackHandler()

# Initialize the Google Gemini LLM with the flash model
# gemini-2.5-flash is optimized for speed and efficiency
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Create a prompt template with a placeholder variable {topic}
# This allows for dynamic prompt generation with different topics
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")

# Create a LangChain chain by piping the prompt into the LLM
# The | operator chains the prompt and model together
chain = prompt | llm

# Invoke the chain with a specific topic and enable Langfuse tracing
# The callbacks parameter ensures all interactions are logged to Langfuse
response = chain.invoke({"topic": "cats"}, config={"callbacks": [langfuse_handler]})

# Print the generated joke from the LLM response
print(response.content)
