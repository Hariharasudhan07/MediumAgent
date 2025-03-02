import os
import json
from dotenv import load_dotenv
from googlesearchagent import NewsSearchAgent
from webscrapagent import WebSearchAgent
from agno.agent import Agent
from agno.models.google import Gemini

def load_api_key():
    """Load and return the Gemini API key from environment variables."""
    load_dotenv()
    return os.getenv('openrouterapi')

def get_search_results(user_query):
    """Search for articles related to the user query using NewsSearchAgent."""
    news_agent = NewsSearchAgent()
    results = news_agent.run(user_query)
    print(f"Found {len(results)} articles related to '{user_query}'.")
    return results

def build_data_store(results):
    """For each result URL, fetch its summary using WebSearchAgent and build a data store."""
    web_agent = WebSearchAgent()
    data_store = []
    for url in results:
        summary = web_agent.search_webpage(url)
        data_store.append({"url": url, "summary": summary})
    print("Data Store:", data_store)
    return data_store

def generate_blog(data_store, apikey):
    """Generate a blog post using the retrieved data_store via an AGNO RAG agent."""
    rag_agent = Agent(
        name="RAG Blog Agent",
        agent_id="rag-agent",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=apikey),
        read_chat_history=True,
        instructions=[
            "Use only the retrieved documents from embeddings.json to generate content.",
            "Ensure the blog is structured concisely with headings.",
            "Use bullet points or tables where necessary.",
            "Need to be humanized and consise with headings.",
            "Use bullet points or tables where necessary.",
            "Use code snippets where necessary.",
            "If there is need of references, use them.",
            "Use images where necessary.",
            "Use examples where necessary.",
            "Use quotes where necessary.",
            "Use statistics where necessary.",
            "Use diagrams where necessary.",
            "Use tables where necessary."
         
        ],
        markdown=True,
    )
    prompt = f"""You are a professional blogger. Write a concise, structured blog using the information below.

### Information:
{data_store}

### Blog:
"""
    blog = rag_agent.run(prompt)
    return blog.content

def main():
    # Load API key and get user query
    apikey = load_api_key()
    user_query = input("Enter a topic to search for: ")

    # Step 1: Search for articles related to the topic
    results = get_search_results(user_query)

    # Step 2: Extract webpage summaries and build the data store
    data_store = build_data_store(results)

    # Step 3: Generate the blog based on the data store
    blog_output = generate_blog(data_store, apikey)

    print("\nGenerated Blog:\n")
    print(blog_output)

    # Optionally, if you want to run the FastAPI playground for further interactions:
    # rag_playground_app = Playground(agents=[rag_agent]).get_app()
    # serve_playground_app("your_module_name:app", reload=True)

if __name__ == "__main__":
    main()
