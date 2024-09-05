from crewai import Agent
from langchain_community.llms import Ollama
from nba_tools import get_nba_all_time_leaders

from config import LLM_LLAMA70B, LLM_LLAMA8B

def create_nba_researcher():
    return Agent(
        role='NBA Researcher',
        goal='Research and retrieve accurate NBA all-time leader statistics',
        backstory="You are an expert NBA researcher with extensive knowledge of basketball history and statistics.",
        llm=LLM_LLAMA8B,
        verbose=True,
        allow_delegation=False,
        tools=[get_nba_all_time_leaders]  # Add this line to include the NBA stats tool
    )

def create_nba_stats_writer():
    return Agent(
        role='NBA Stats Writer',
        goal='Write clear and engaging summaries of NBA all-time leader statistics',
        backstory="You are a skilled sports writer specializing in presenting complex NBA statistics in an accessible and interesting manner.",
        llm=LLM_LLAMA70B,
        verbose=True,
        allow_delegation=False
    )