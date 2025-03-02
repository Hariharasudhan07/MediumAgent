from agno.agent import Agent
from agno.tools.website import WebsiteTools
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('geminiapi')

class WebSearchAgent:
    def __init__(self):
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp", api_key=apikey),
            tools=[WebsiteTools()],
            show_tool_calls=True
        )

    def search_webpage(self, url: str):
        print(f"Searching webpage: {url}")  # Debugging
        # Use run() to instruct the agent to extract the webpage content.
        response = self.agent.run(f"Search web page: '{url}' and give me a summary of around 500 words.")
        print(f"Response content: {response.content}")  # Debugging
        return response.content

# Example usage:
# if __name__ == "__main__":
#     search_agent = WebSearchAgent()
#     webpage_url = "https://docs.agno.com/introduction"
#     content = search_agent.search_webpage(webpage_url)
#     print("Extracted Content:\n", content)
