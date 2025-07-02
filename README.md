📚 Virtual Research Assistant
A Streamlit-based application that helps researchers find, summarize, and analyze academic papers on any given topic using AI agents.


Features
🔍 Fetches research papers from ArXiv (and potentially Google Scholar)
📝 Generates concise summaries of research papers
⚖️ Analyzes advantages and disadvantages of each paper
🚀 Fast processing using Groq API
🌐 Simple web interface with Streamlit


Requirements
Python 3.7+
Streamlit
python-dotenv
Groq API key
Installation https://github.com/bittush8789/AI-Powered-Research-Assistant.git
cd virtual-research-assistant
pip install -r requirements.txt

GROQ_API_KEY=your_api_key_here

streamlit run app.py

virtual-research-assistant/ ├── app.py # Main Streamlit application ├── agents.py # AI agents for summarization and analysis ├── data_loader.py # Handles fetching papers from various sources ├── .env # Environment variables (ignored in git) ├── requirements.txt # Python dependencies └── README.md # This file