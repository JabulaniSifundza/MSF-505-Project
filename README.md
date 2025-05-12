# AI-Powered Stock News Sentiment Analysis & Insight Generation

This project provides a Python script to automate the process of gathering recent financial news for specific stock tickers, extracting the article content, and using a Large Language Model (LLM) via Langchain to analyze the sentiment and potential implications for stock prices.

The script leverages web scraping techniques to pull news links related to target tickers from a designated source (via Google News search targeting Finviz) and then uses an LLM to provide a qualitative analysis of the aggregated news sentiment from the scraped articles.

## Features

* **Targeted News Retrieval:** Automatically searches for relevant financial news articles for specified stock tickers.
* **Source-Specific Search:** Configured to prioritize news links originating from Finviz, found via Google News search.
* **Article Content Extraction:** Scrapes the text content from the retrieved news article URLs.
* **LLM-Based Sentiment Analysis:** Utilizes the Google Gemini model via Langchain to analyze the collective sentiment of the scraped articles.
* **Investment Insight Generation:** Prompts the LLM to provide potential insights into how the news sentiment might affect stock prices from the perspective of an analytical financial analyst.
* **Scalable:** Easily adaptable to analyze multiple tickers by modifying a list.

## Requirements

* Python 3.7+
* `beautifulsoup4` (`bs4`)
* `requests`
* `pandas`
* `numpy`
* `langchain-google-genai`
* `langchain_community`
* `langgraph`
* `urllib3` (often installed with requests, but good to list if issues arise)
* A **Google Cloud API Key** with access to Generative AI models (specifically `gemini-2.0-flash`).

## Installation

1.  Clone this repository (or copy the script).
2.  Navigate to the project directory in your terminal.
3.  Install the required Python libraries:

    ```bash
    pip install beautifulsoup4 requests pandas numpy langchain-google-genai langchain_community langgraph urllib3
    ```

## Setup

1.  **Obtain a Google Cloud API Key:** You need an API key with permissions to use Google's Generative AI models (like Gemini). You can obtain one from the Google Cloud Console or the Google AI Studio.
2.  **Insert API Key:** Open the script (`your_script_name.py`) and locate the line initializing the `ChatGoogleGenerativeAI` model:
    ```python
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key="API KEY GOES HERE")
    ```
    Replace `"API KEY GOES HERE"` with your actual API key.

    * **Security Note:** Hardcoding API keys directly in scripts is generally not recommended for production environments. For better security, consider using environment variables (`os.environ.get('GOOGLE_API_KEY')`) or a dedicated secrets management tool. For simplicity in this script, it's hardcoded, but be mindful of this in larger projects.

## Usage

1.  **Configure Tickers:** Open the script (`your_script_name.py`) and modify the `research_tickers` list to include the stock tickers you want to analyze:
    ```python
    research_tickers = ['AMZN', 'GOOGL', 'MSFT'] # Example: Add more tickers here
    ```
2.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python your_script_name.py
    ```

The script will perform the following steps:
* For each ticker, search Google News for articles mentioning the ticker from Finviz.
* Clean the retrieved URLs.
* Visit each cleaned URL and scrape the first ~350 words of paragraph text.
* Pass the collected article snippets for all tickers to the Langchain agent configured with the Gemini model.
* The LLM agent will analyze the text for sentiment and potential stock price impact based on its persona.
* The LLM's analysis will be printed to the console.

## How it Works

1.  **News Search:** The `get_news` function constructs a Google News search query targeting Finviz articles for each ticker.
2.  **URL Extraction & Cleaning:** It scrapes the Google search results page to extract potential article URLs, then filters and cleans them to remove unwanted links (like Google internal links).
3.  **Article Scraping:** The `scrape_and_read_articles` function iterates through the cleaned URLs, fetches the HTML content, extracts all paragraph text, joins it, and truncates the result to approximately the first 350 words.
4.  **LLM Analysis:** The collected article snippets are formatted into a dictionary. This dictionary is passed to a Langchain `JsonToolkit` and `JsonAgent`. The agent uses the configured LLM (Gemini) to read the JSON data (the article snippets) and responds to a prompt requesting a financial analyst's sentiment analysis and insights.

## Limitations

* **Reliance on External Sites:** The script's functionality depends heavily on the structure of Google Search results and the HTML structure of news articles on various websites linked via Finviz. Changes to these sites can break the scraping logic.
* **Truncated Articles:** Only the first ~350 words of each article are scraped. This might lead to missing crucial context or sentiment expressed later in longer articles.
* **Scraping Robustness:** Basic `requests` and `BeautifulSoup` might struggle with dynamic websites or sites with aggressive anti-scraping measures.
* **News Source Flexibility:** Currently hardcoded to search for Finviz news via Google. Modifying the target source requires code changes.
* **Error Handling:** Error handling is basic (a `try...except` around the LLM call). More robust error handling for network issues, scraping failures, etc., could be added.
* **LLM Cost & Rate Limits:** Repeatedly running the script with multiple tickers and articles will incur costs associated with the LLM usage and may hit API rate limits.
* **Sentiment Nuance:** LLM analysis, while powerful, can be subjective. The quality and relevance of insights depend on the LLM's capabilities and the prompt/persona provided.

## Contributing

Contributions are welcome! If you find a bug or have an idea for improvement, please open an issue or submit a pull request.

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]
