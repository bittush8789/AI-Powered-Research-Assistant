# Importing required libraries
import requests  # For sending HTTP requests to fetch data from external sources (like ArXiv)
import xml.etree.ElementTree as ET  # For parsing XML responses (ArXiv returns XML)
from scholarly import scholarly  # For searching and scraping academic papers from Google Scholar

# Define the DataLoader class which encapsulates methods to fetch research papers
class DataLoader:
    """
    DataLoader is responsible for fetching academic papers from external sources
    like ArXiv and Google Scholar.
    """

    def __init__(self):
        # Constructor method that prints a message when the class is instantiated
        print("DataLoader Init")

    def fetch_arxiv_papers(self, query):
        """
        Fetches up to 5 relevant research papers from ArXiv based on a user query.
        If fewer than 5 papers are found, the method attempts to expand the search
        using related research topics suggested by an AI agent (if defined).

        Args:
            query (str): The search term or topic to look for in ArXiv.

        Returns:
            list: A list of dictionaries, each containing 'title', 'summary', and 'link'.
        """

        # Nested helper function to query the ArXiv API
        def search_arxiv(query):
            """
            Internal helper function to search ArXiv for the given query.

            Args:
                query (str): The keyword/topic to search in ArXiv.

            Returns:
                list: List of paper metadata dictionaries if successful; otherwise an empty list.
            """
            # Construct the API URL with the given query, limiting to 5 results
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"

            # Make the HTTP GET request to ArXiv API
            response = requests.get(url)

            # Check for a successful response
            if response.status_code == 200:
                # Parse the XML content returned from ArXiv
                root = ET.fromstring(response.text)

                # Extract relevant information (title, summary, link) from each entry
                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]

            # Return an empty list if the request failed
            return []

        # Initial paper search with the user query
        papers = search_arxiv(query)

        # If fewer than 5 papers are found and a search agent is defined
        if len(papers) < 5 and hasattr(self, 'search_agent'):
            # Use the search agent (likely an LLM) to suggest related research topics
            related_topics_response = self.search_agent.generate_reply(
                messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
            )

            # Extract the text content and split by lines (each line = a related topic)
            related_topics = related_topics_response.get("content", "").split("\n")

            # Iterate through suggested topics and fetch more papers
            for topic in related_topics:
                topic = topic.strip()  # Clean whitespace

                # If topic is not empty and we still have <5 papers, search again
                if topic and len(papers) < 5:
                    new_papers = search_arxiv(topic)
                    papers.extend(new_papers)  # Add new results to existing list

                    # Trim the list to ensure we only return max 5 papers
                    papers = papers[:5]

        # Return the final list of papers
        return papers

    def fetch_google_scholar_papers(self, query):
        """
        Fetches the top 5 research papers from Google Scholar using the `scholarly` API.

        Args:
            query (str): The keyword or topic to search for.

        Returns:
            list: A list of dictionaries, each containing 'title', 'summary', and 'link'.
        """

        papers = []  # Initialize the result list

        # Use scholarly to perform the search (returns a generator)
        search_results = scholarly.search_pubs(query)

        # Iterate through results and collect up to 5 papers
        for i, paper in enumerate(search_results):
            if i >= 5:
                break  # Stop if we've collected 5 papers

            # Append the paper details to the result list
            papers.append({
                "title": paper["bib"]["title"],  # Title of the paper
                "summary": paper["bib"].get("abstract", "No summary available"),  # Abstract if available
                "link": paper.get("pub_url", "No link available")  # Publication link (if any)
            })

        # Return the final list of papers
        return papers
