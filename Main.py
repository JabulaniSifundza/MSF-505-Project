import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import JsonToolkit, create_json_agent
from langchain_community.tools.json.tool import JsonSpec
'''
We use Fin Viz as our news source
url = "https://finviz.com/news.ashx"
req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(req).read()
html = soup(webpage, "html.parser")

# News scrape function:
    
def scrape(link, indx):
    try:
        news = pd.read_html(str(html))[indx]
        news.columns = ["0", "Time", "Headlines"]
        news = news.drop(columns=["0"])
        news = news.set_index("Time")
        print(news)
        return news
    except Exception as e:
        print(f"Error: {e}")
        return None
    
news_df = scrape(html, 3)
'''
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key="API KEY GOES HERE")
research_tickers = ['AMZN']
# Running a Google search on the desired Ticker Symbol;
# We are specifically looking for articles from our news source
def get_news(ticker):
    news_source = "https://www.google.com/search?q=finviz+news+{}&tbm=nws".format(ticker)
    r = requests.get(news_source)
    soup = BeautifulSoup(r.text, 'html.parser')
    linktags = soup.find_all('a')
    hrefs = [link['href'] for link in linktags]
    return hrefs

# Getting links to articles
article_links = {ticker:get_news(ticker) for ticker in research_tickers}
# Cleaning up and formatting article URLS
unwanted_string_list = ['maps', 'policies', 'preferences', 'accounts', 'support']
def remove_unwanted_strings(urls, unwanted_string):
    new_urls = []
    for url in urls:
        if 'https://' in url and not any(exclude_word in url for exclude_word in unwanted_string):
            res = re.findall(r'(https?://\S+)', url)[0].split('&')[0]
            new_urls.append(res)
    return list(set(new_urls))

cleaned_urls = {ticker:remove_unwanted_strings(article_links[ticker], unwanted_string_list) for ticker in research_tickers}
# print(cleaned_urls)
cleanArr = [cleaned_urls]
for link in cleanArr:
    values = link.values()
    # print(values)
    for val in values:
        urlText = val
        for text in urlText:
            print(text)
            
# Sraping news articles and their content            
def scrape_and_read_articles(URLs):
    NEWS_ARTICLES = []
    for url in URLs:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraph_text = [paragraph.text for paragraph in paragraphs]
        words = ' '.join(paragraph_text).split(' ')[:350]
        full_article = ' '.join(words)
        NEWS_ARTICLES.append(full_article)
    return NEWS_ARTICLES

articles = {ticker:scrape_and_read_articles(cleaned_urls[ticker]) for ticker in research_tickers}
print(articles)

# Using the LLM to analyze scraped articles in JSON Format
system_message = "You are a highly analytical financial analyst looking for companies to invest in. Investments can be long or short positions. Analyze the sentiment of the text and how it might affect stock prices in the near future.."
try:
    json_spec = JsonSpec(dict_=articles, max_value_length=8000)
    json_toolkit = JsonToolkit(spec=json_spec)
    json_agent_executor = create_json_agent(
        llm=model, toolkit=json_toolkit, verbose=True
    )
    results = json_agent_executor.run(
        "As a highly analytical financial analyst for an options trading firm, what are your thoughts on the sentiment of the given articles."
    )
    print(results)
except Exception as Err:
    print(Err)



