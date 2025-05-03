from yahooquery import Ticker
import pandas_datareader as pdr
from google import genai
import datetime
import numpy as np
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_core.prompts import PromptTemplate
from sec_api import QueryApi
import requests 
import json

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key="API KEY GOES HERE")
# Langchain Tool for analysis
tools = [YahooFinanceNewsTool()]
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
# agent_chain.invoke(
#    "What happened today with Microsoft stocks?",
# )
tool = YahooFinanceNewsTool()
# res = tool.invoke("AAPL")
# print(res)

TICKERS = ["AAPL", "TSLA", "MSFT", "AMZN"]
news_articles = []

for ticker in TICKERS:
    # agent_chain.invoke(f"What happened today with {ticker} stocks?")
    news = tool.invoke(ticker)
    news_articles.append(news)
    print(news_articles)
    
for news_story in news_articles:
    template = """Question: {question}
    
    Answer: Let's think step by step from the lens of a highly analytical financial analyst 
    looking for companies to invest in. 
    Investments can be long or short positions. Analyze the sentiment of the text 
    and how it might affect stock prices in the near future."""
    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | llm
    
    question = f"What's your outlook on {news_story}?"
    answer = chain.invoke({"question": question})
    print(answer)
