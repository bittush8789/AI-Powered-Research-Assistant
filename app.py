# Import required libraries
import streamlit as st  # Streamlit for building the web interface
import os  # For accessing environment variables
from dotenv import load_dotenv  # To load variables from a .env file
from agents import ResearchAgents  # Custom module for AI agents
from data_loader import DataLoader  # Custom module for fetching research data

# Load environment variables from the .env file into the environment
load_dotenv()

print("ok")  # Debug message to indicate script has started

# Set the title of the Streamlit web app
st.title("📚 Virtual Research Assistant")

# Get the GROQ API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# If the API key is missing, show an error message and stop execution
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize the ResearchAgents class with the provided API key
agents = ResearchAgents(groq_api_key)

# Initialize the DataLoader class for fetching papers from ArXiv / Scholar
data_loader = DataLoader()

# Create a text input box for the user to type their research query
query = st.text_input("Enter a research topic:")

# When the user clicks the "Search" button
if st.button("Search"):
    # Show a loading spinner while data is being fetched
    with st.spinner("Fetching research papers..."):
        
        # Fetch top research papers from ArXiv based on the query
        arxiv_papers = data_loader.fetch_arxiv_papers(query)

        # Optional: Could include Google Scholar as well (currently commented out)
        # google_scholar_papers = data_loader.fetch_google_scholar_papers(query)
        # all_papers = arxiv_papers + google_scholar_papers
        all_papers = arxiv_papers  # Use only ArXiv for now

        # If no papers were found, display an error
        if not all_papers:
            st.error("Failed to fetch papers. Try again!")
        else:
            processed_papers = []  # List to store processed paper data

            # Loop over each paper to summarize and analyze
            for paper in all_papers:
                summary = agents.summarize_paper(paper['summary'])  # Summarize paper content
                adv_dis = agents.analyze_advantages_disadvantages(summary)  # Get pros and cons

                # Store results in a structured format
                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })

            # Display the list of processed research papers
            st.subheader("Top Research Papers:")

            # Render each paper with title, link, summary, and analysis
            for i, paper in enumerate(processed_papers, 1):
                st.markdown(f"### {i}. {paper['title']}")  # Paper title
                st.markdown(f"🔗 [Read Paper]({paper['link']})")  # Link to full paper
                st.write(f"**Summary:** {paper['summary']}")  # Paper summary
                st.write(f"{paper['advantages_disadvantages']}")  # Pros and cons
                st.markdown("---")  # Separator between papers
