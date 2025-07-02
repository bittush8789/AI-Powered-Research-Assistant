# Importing required libraries
import requests  # For sending HTTP requests to external APIs
import xml.etree.ElementTree as ET  # For parsing XML responses from ArXiv
from scholarly import scholarly  # For scraping/searching Google Scholar data

class DataLoader:
    """
    DataLoader is responsible for fetching academic papers from external sources
    like ArXiv and Google Scholar.
    """

    def __init__(self):
        print("DataLoader Init")  # Simple initializer log

    def fetch_arxiv_papers(self, query):
        """
        Fetches up to 5 relevant research papers from ArXiv based on a query.
        If fewer than 5 papers are found, it tries to expand the search using related topics.
        
        Args:
            query (str): Search keyword/topic
        
        Returns:
            list: A list of dictionaries with paper 'title', 'summary', and 'link'
        """

        def search_arxiv(query):
            """
            Queries the ArXiv API for research papers based on the input query.
            
            Args:
                query (str): Search keyword

            Returns:
                list: Parsed list of paper metadata from XML
            """
            # Building the API request URL
            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
            response = requests.get(url)  # Send request to ArXiv

            # If request is successful, parse XML response
            if response.status_code == 200:
                root = ET.fromstring(response.text)  # Parse XML content

                # Extract relevant fields (title, summary, link) from each entry
                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]

            # If API call fails, return empty list
            return []

        papers = search_arxiv(query)  # Initial search based on original query

        # Check if fewer than 5 papers are returned and if search_agent is defined
        if len(papers) < 5 and hasattr(self, 'search_agent'):
            # Ask the search agent to suggest related topics to broaden the search
            related_topics_response = self.search_agent.generate_reply(
                messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
            )

            # Parse agent response – expects a newline-separated list of topics
            related_topics = related_topics_response.get("content", "").split("\n")

            # Loop through related topics and attempt to fetch more papers
            for topic in related_topics:
                topic = topic.strip()
                if topic and len(papers) < 5:
                    new_papers = search_arxiv(topic)
                    papers.extend(new_papers)
                    papers = papers[:5]  # Ensure the list doesn’t exceed 5 items

        return papers  # Final list of up to 5 papers

    def fetch_google_scholar_papers(self, query):
        """
        Fetches top 5 research papers from Google Scholar using the `scholarly` package.
        
        Args:
            query (str): Topic or keyword
        
        Returns:
            list: A list of dictionaries with 'title', 'summary', and 'link'
        """
        papers = []  # Result list to be returned

        # Perform the search using scholarly API
        search_results = scholarly.search_pubs(query)

        # Loop through results and collect paper info (limit to 5)
        for i, paper in enumerate(search_results):
            if i >= 5:
                break  # Stop after collecting 5 papers

            papers.append({
                "title": paper["bib"]["title"],
                "summary": paper["bib"].get("abstract", "No summary available"),
                "link": paper.get("pub_url", "No link available")
            })

        return papers  # Return the collected paper list
