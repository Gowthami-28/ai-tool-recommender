import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load API key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Retry config — valid in ADK 2.3.0
retry_config = types.HttpRetryOptions(
    attempts=3,          # 5 is excessive; 3 is enough
    exp_base=2,          # exp_base=7 is too aggressive (7^1=7s, 7^2=49s wait)
    initial_delay=2,
    http_status_codes=[429, 500, 503, 504]
)

root_agent = Agent(
    name="ai_tool_recommender",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    description="An agent that recommends AI tools for business owners.",
    instruction="""You are an expert AI tools consultant for business owners.
    When a user describes their business problem:
    1. Analyze what kind of problem it is
    2. Recommend 3 specific AI tools that solve it
    3. Explain WHY each tool fits their specific problem
    4. Give one practical next step to get started
    Be specific, practical and helpful.""",
)

async def main():
    runner = InMemoryRunner(agent=root_agent)
    
    print("Running AI Tool Recommender...\n")
    
    user_query = input("Describe your business problem: ")
    events = await runner.run_debug(user_query)
    
    # Extract and print the final response
    for event in events:
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print("Agent Response:\n")
                    print(part.text)

if __name__ == "__main__":
    asyncio.run(main())