from langchain_community.retrievers import TavilySearchAPIRetriever
import os 
import subprocess

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
subprocess.run(
        f'export TAVILY_API_KEY="{TAVILY_API_KEY}"',
        shell=True,
        executable="/bin/bash",
        check=True
    )
# 1. Instantiate the Tavily retriever (fetches top 5 results by default)
tavily_retriever = TavilySearchAPIRetriever(k=5)

# 2. Wrap it in a function
def search_internet(query: str) -> str:
    """
    Query the web via Tavily Search API and return formatted snippets.
    """
    docs = tavily_retriever.invoke(query)
    results = []
    for d in docs:
        title  = d.metadata.get("title", "").strip()
        source = d.metadata.get("source", "").strip()
        snippet = d.page_content.replace("\n", " ").strip()
        results.append(f"{title}\n{snippet}\n— {source}")
    return "\n\n".join(results)