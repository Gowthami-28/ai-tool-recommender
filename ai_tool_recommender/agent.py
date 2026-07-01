"""
AI Tool Recommender Agent
=========================
Built using Google Agent Development Kit (ADK) v2.3.0 with Gemini 2.5 Flash.

Architecture:
- Agent: Single LLM agent with a consultant persona defined via system instruction
- Runner: InMemoryRunner for local CLI execution via `adk run` or `python agent.py`
- Model: Gemini 2.5 Flash with exponential backoff retry for 429/5xx errors
- Input: Interactive terminal prompt — user describes their business problem
- Output: 3 AI tool recommendations with justification and a practical next step

ADK Concepts Demonstrated:
1. Agent/Multi-agent system — root_agent defined with ADK Agent class
2. Agent Skills / CLI — runnable via `adk run ai_tool_recommender`
3. Antigravity IDE — developed and tested inside Antigravity workspace
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load GOOGLE_API_KEY from .env file (never hardcode API keys in source)
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Retry configuration for transient API failures
# - attempts=3: retries up to 3 times before raising an error
# - exp_base=2: exponential backoff waits 2s, 4s, 8s between retries
# - initial_delay=2: first retry waits 2 seconds
# - http_status_codes: retries on quota exceeded (429) and server errors (5xx)
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=2,
    http_status_codes=[429, 500, 503, 504]
)

# Define the root agent
# - name: Python identifier used by ADK CLI (`adk run ai_tool_recommender`)
# - model: Gemini 2.5 Flash with retry config attached
# - instruction: system prompt that defines agent behavior and output format
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
    2. Recommend 3 specific AI tools that solve it — prioritize lesser-known,
       specialized tools over generic ones like ChatGPT or Canva unless they
       are genuinely the best fit
    3. Explain WHY each tool fits their specific problem
    4. Give one practical next step to get started
    Be specific, practical and helpful.""",
)


async def main():
    """
    Entry point for the AI Tool Recommender agent.

    Initializes an InMemoryRunner with the root agent, accepts a business
    problem description from the user via terminal input, runs the agent,
    and prints the final response extracted from the event stream.
    """
    runner = InMemoryRunner(agent=root_agent)

    print("Running AI Tool Recommender...\n")

    # Get user input and validate — empty queries waste API quota
    user_query = input("Describe your business problem: ").strip()
    if not user_query:
        print("No input provided. Please describe a business problem.")
        return

    # Run the agent and collect all events from the response stream
    events = await runner.run_debug(user_query)

    # Extract final response from event stream
    # is_final_response() identifies the last agent turn
    # event.content.parts contains the text blocks of the response
    for event in events:
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print("\nAgent Response:\n")
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())