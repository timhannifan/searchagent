"""Simple implementation of an agent."""

import argparse

import requests
from dotenv import load_dotenv
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    LiteLLMModel,
    Tool,
    ToolCallingAgent,
    VisitWebpageTool,
    tool,
)

AUTHORIZED_IMPORTS = [
    "os",
    "pandas",
    "requests",
    "datetime",
]

load_dotenv(override=True)
custom_role_conversions = {"tool-call": "assistant", "tool-response": "user"}

def parse_args():
    """Parses command-line arguments for the agent."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "question", type=str, help="for example: 'What is the date?'"
    )
    parser.add_argument("--model-id", type=str, default="gpt-4o-mini")
    return parser.parse_args()

@tool
def search_wikipedia(query: str) -> str:
    """Fetches a summary of a Wikipedia page for a given query.

    Args:
        query: The search term to look up on Wikipedia.

    Returns:
        str: A summary of the Wikipedia page if successful, or an error message if the request fails.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        title = data["title"]
        extract = data["extract"]

        return f"Summary for {title}: {extract}"

    except requests.exceptions.RequestException as e:
        return f"Error fetching Wikipedia data: {str(e)}"

image_generation_tool = Tool.from_space(
    # "black-forest-labs/FLUX.1-schnell",
    # "multimodalart/stable-cascade",
    "black-forest-labs/FLUX.1-dev",
    name="image_generator",
    description="Generate an image from a prompt"
)

def query_agent(query, model_id="gpt-4o-mini"):
    """Run the agent with a specific question."""
    model = LiteLLMModel(
        model_id=model_id,
        custom_role_conversions=custom_role_conversions,
    )

    web_search_agent = ToolCallingAgent(
        model=model,
        tools=[DuckDuckGoSearchTool(), VisitWebpageTool(), search_wikipedia],
        max_steps=3,
        verbosity_level=2,
        planning_interval=5,
        name="search",
        description="A team member that will search the internet to answer your question.",
        provide_run_summary=True,
    )

    manager_agent = CodeAgent(
        model=model,
        tools=[image_generation_tool],
        max_steps=10,
        verbosity_level=2,
        planning_interval=5,
        additional_authorized_imports=AUTHORIZED_IMPORTS,
        managed_agents=[web_search_agent],
    )

    answer = manager_agent.run(query)

    return answer

def main():
    """Main function to run the agent."""
    args = parse_args()
    answer = query_agent(args.question, args.model_id)
    print(f"Got this answer: {answer}")

if __name__ == "__main__":
    main()