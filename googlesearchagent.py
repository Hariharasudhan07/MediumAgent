import json
from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools

class NewsSearchAgent(Agent):
    def __init__(self):
        super().__init__()
        self.search_tool = GoogleSearchTools()

    def run(self, topic: str):
        query = f"Top news articles about {topic}"
        results = self.search_tool.google_search(query=query, max_results=5)

        # Debugging output
        # print("DEBUG: Raw search results:", results)

        # Handle different result formats
        if isinstance(results, str):  # If results is a JSON string, parse it
            try:
                results = json.loads(results)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON response")

        if isinstance(results, dict) and 'items' in results:  # If results is a dict, extract 'items'
            results = results.get('items', [])

        if not isinstance(results, list):
            raise ValueError(f"Unexpected search results format: {type(results)} - {results}")

        return [result.get('url', 'No URL found') for result in results]

# Run the agent
# agent = NewsSearchAgent()
# topic = input("Enter a topic to search for: ")
# results = agent.run(topic)
# for i in results:
#     print(i)

