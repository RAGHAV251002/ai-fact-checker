import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_claim(claim: str):
    """
    Search the web for evidence related to a claim.
    """

    response = client.search(

        query=claim,

        search_depth="advanced",

        max_results=5,

        include_answer=True,

        include_raw_content=False

    )

    return response