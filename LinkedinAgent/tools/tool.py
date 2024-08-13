from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_with_url_Tavily(query: str):
    """Searches for linkedin pages or twitter profle pages"""
    try:
        search = TavilySearchResults()
        result = search.run(tool_input=f"{query}")
        if not result:
            print("URL found this iteration is NONE")
            return None
        return result[0]["url"]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
