from crewai import Agent
from config import LLM_LLAMA70B, LLM_LLAMA8B, LLM_GEMMA2, LLM_MIXTRAL
from nba_tools import get_nba_game_info, get_nba_player_stats, get_nba_all_time_leaders

def create_nba_researcher():
    return Agent(
        llm=LLM_LLAMA70B,
        role="NBA Researcher",
        goal="Identify and return info for NBA games and all-time statistics",
        backstory="An NBA researcher that identifies games for statisticians to analyze stats from and can also provide historical statistical information",
        tools=[get_nba_game_info, get_nba_all_time_leaders],
        verbose=True,
        allow_delegation=False
    )

def create_nba_statistician():
    return Agent(
        llm=LLM_LLAMA70B,
        role="NBA Statistician",
        goal="Retrieve player stats for the game identified by the NBA Researcher",
        backstory="An NBA Statistician analyzing player boxscore stats for the relevant game",
        tools=[get_nba_player_stats],
        verbose=True,
        allow_delegation=False
    )

def create_nba_writer_llama():
    return Agent(
        llm=LLM_LLAMA8B,
        role="NBA Writer",
        goal="Write a detailed game recap article using the provided game information and stats",
        backstory="An experienced and honest writer who does not make things up",
        tools=[],
        verbose=True,
        allow_delegation=False
    )

def create_nba_writer_gemma():
    return Agent(
        llm=LLM_GEMMA2,
        role="NBA Writer",
        goal="Write a detailed game recap article using the provided game information and stats",
        backstory="An experienced and honest writer who does not make things up",
        tools=[],
        verbose=True,
        allow_delegation=False
    )

def create_nba_writer_mixtral():
    return Agent(
        llm=LLM_MIXTRAL,
        role="NBA Writer",
        goal="Write a detailed game recap article using the provided game information and stats",
        backstory="An experienced and honest writer who does not make things up",
        tools=[],
        verbose=True,
        allow_delegation=False
    )

def create_nba_editor():
    return Agent(
        llm=LLM_LLAMA70B,
        role="NBA Editor",
        goal="Edit multiple game recap articles to create the best final product.",
        backstory="An experienced editor that excels at taking the best parts of multiple texts to create the best final product",
        tools=[],
        verbose=True,
        allow_delegation=False
    )

def create_nba_stats_writer():
    return Agent(
        llm=LLM_LLAMA8B,
        role="NBA Stats Writer",
        goal="Write a clear, concise summary of NBA all-time leaders in a specific statistical category",
        backstory="An experienced sports writer who can translate raw stats into engaging, informative content",
        tools=[],
        verbose=True,
        allow_delegation=False
    )