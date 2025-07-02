
# Virtual Research Assistant

A Streamlit-based application designed to assist researchers in discovering, summarizing, and analyzing academic papers on any given topic using AI agents.

## Features

- Fetches research papers from ArXiv (with potential integration for Google Scholar)
- Generates concise summaries of research papers
- Analyzes advantages and disadvantages of each paper
- Utilizes Groq API for fast processing
- Provides a simple web interface with Streamlit

## Requirements

- Python 3.7+
- Streamlit
- python-dotenv
- Groq API key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/bittush8789/Autogen_Project.git
   cd Autogen_Project
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory.
   - Add your Groq API key:
     ```env
     GROQ_API_KEY=your_api_key_here
     ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

Once the application is running:
- Enter a research topic in the input field.
- Click on "Search" to fetch relevant research papers.
- View the summarized information along with advantages and disadvantages for each paper.

## Project Structure

- `app.py` - Main application file for Streamlit.
- `agents.py` - Contains AI agents for summarization and analysis.
- `data_loader.py` - Handles fetching of research papers from external sources.
- `requirements.txt` - Lists all Python dependencies.
- `.env` - Stores environment variables (not included in the repository).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
