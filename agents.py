# Import necessary libraries
import os  # For interacting with the operating system (e.g., accessing environment variables)
from autogen import AssistantAgent  # Importing AssistantAgent from autogen framework
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from .env into the runtime environment
load_dotenv()

# Define the ResearchAgents class to handle LLM agents for summarization and analysis
class ResearchAgents:
    def __init__(self, api_key):
        """
        Initializes the research assistant agents using the given Groq API key.
        Sets up two agents:
            1. summarizer_agent - summarizes research papers
            2. advantages_disadvantages_agent - provides pros and cons
        """

        # Store API key locally for use in agent configuration
        self.groq_api_key = api_key

        # Define LLM configuration for Groq API using LLaMA model
        self.llm_config = {
            'config_list': [{
                'model': 'deepseek-r1-distill-llama-70b',  # deepseek-r1-distill-llama-70b
                'api_key': self.groq_api_key,       # Provided API key
                'api_type': "groq"                  # API provider type
            }]
        }

        # Create the summarizer agent with a strict summarization system message
        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",  # Unique name for the agent
            system_message=(
                "Summarize the retrieved research papers and present concise summaries to the user, "
                "JUST GIVE THE RELEVANT SUMMARIES OF THE RESEARCH PAPER AND NOT YOUR THOUGHT PROCESS."
            ),
            llm_config=self.llm_config,      # LLM model and API configuration
            human_input_mode="NEVER",        # Agent should not expect user follow-ups
            code_execution_config=False      # No code execution needed
        )

        # Create the advantages/disadvantages agent with a separate system message
        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",  # Unique agent name
            system_message=(
                "Analyze the summaries of the research papers and provide a list of advantages and disadvantages "
                "for each paper in a pointwise format. JUST GIVE THE ADVANTAGES AND DISADVANTAGES, NOT YOUR THOUGHT PROCESS"
            ),
            llm_config=self.llm_config,      # Same LLM config as summarizer
            human_input_mode="NEVER",        # No back-and-forth input expected
            code_execution_config=False      # Code execution not required
        )

    def summarize_paper(self, paper_summary):
        """
        Uses the summarizer_agent to generate a concise summary of the given paper.

        Args:
            paper_summary (str): Full or partial content of a research paper.

        Returns:
            str: A clean, user-friendly summary or an error message if failed.
        """
        summary_response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": f"Summarize this paper: {paper_summary}"}]
        )

        # Return content if successful, otherwise return error fallback
        return summary_response.get("content", "Summarization failed!") \
            if isinstance(summary_response, dict) else str(summary_response)

    def analyze_advantages_disadvantages(self, summary):
        """
        Uses the advantages_disadvantages_agent to extract pros and cons from the summary.

        Args:
            summary (str): The summarized research paper content.

        Returns:
            str: Point-wise advantages and disadvantages, or error message if failed.
        """
        adv_dis_response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": f"Provide advantages and disadvantages for this paper: {summary}"}]
        )

        # Return the analysis if present; otherwise return error fallback
        return adv_dis_response.get("content", "Advantages and disadvantages analysis failed!")
