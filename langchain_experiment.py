import os
os.environ['OPENAI_API_KEY'] = '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'
os.environ['SERPAPI_API_KEY']="426c3fd2b81ff094bbd77625d0a264e6fe5a6a00f1a1991458e50205bc9a766d"

from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

import requests
from bs4 import BeautifulSoup

def search_statmuse(query: str) -> str:
  URL = f'https://www.statmuse.com/nba/ask/{query}'
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")
  return soup.find("h1", class_="nlg-answer").text

statmuse_tool = Tool(
    name = "Statmuse",
    func = search_statmuse,
    description = "A sports search engine. Use this more than normal search if the question is about NBA basketball, like 'who is the highest scoring player in the NBA?'. Always specify a year or timeframe with your search. Only ask about one player or team at a time, don't ask about multiple players at once."
)

llm = OpenAI(temperature=0)

tools = load_tools(["serpapi", "llm-math"], llm=llm) + [statmuse_tool]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Question
question = "Who has scored more points in the NBA this season, Jayson Tatum or Luka Doncic? Can you subtract the difference in points between them?"
print(question)
agent.run(question)