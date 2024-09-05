from datetime import datetime, timedelta
from crews import create_game_info_crew, create_player_stats_crew
from config import LLM_LLAMA70B, LLM_LLAMA8B, LLM_GEMMA2, LLM_MIXTRAL
from agents import (
    create_nba_researcher, create_nba_statistician, create_nba_writer_llama,
    create_nba_writer_gemma, create_nba_writer_mixtral, create_nba_editor,
    create_nba_stats_writer
)
from tasks import (
    create_collect_game_info_task, create_retrieve_player_stats_task,
    create_write_game_recap_llama_task, create_write_game_recap_gemma_task,
    create_write_game_recap_mixtral_task, create_edit_game_recap_task,
    create_get_all_time_leaders_task, create_write_all_time_leaders_summary_task
)
from crewai import Crew

def route_prompt(user_prompt):
    all_time_keywords = ['all-time', 'all time', 'leader', 'record', 'history', 'career']
    return 'player_stats' if any(keyword in user_prompt.lower() for keyword in all_time_keywords) else 'game_info'

def create_game_info_crew():
    nba_researcher = create_nba_researcher()
    nba_statistician = create_nba_statistician()
    nba_writer_llama = create_nba_writer_llama()
    nba_writer_gemma = create_nba_writer_gemma()
    nba_writer_mixtral = create_nba_writer_mixtral()
    nba_editor = create_nba_editor()

    return Crew(
        agents=[nba_researcher, nba_statistician, nba_writer_llama, nba_writer_gemma, nba_writer_mixtral, nba_editor],
        tasks=[
            create_collect_game_info_task(nba_researcher),
            create_retrieve_player_stats_task(nba_statistician),
            create_write_game_recap_llama_task(nba_writer_llama),
            create_write_game_recap_gemma_task(nba_writer_gemma),
            create_write_game_recap_mixtral_task(nba_writer_mixtral),
            create_edit_game_recap_task(nba_editor)
        ],
        verbose=False
    )

def create_player_stats_crew():
    nba_researcher = create_nba_researcher()
    nba_stats_writer = create_nba_stats_writer()

    get_all_time_leaders_task = create_get_all_time_leaders_task(nba_researcher)
    write_all_time_leaders_summary_task = create_write_all_time_leaders_summary_task(nba_stats_writer, get_all_time_leaders_task)

    return Crew(
        agents=[nba_researcher, nba_stats_writer],
        tasks=[get_all_time_leaders_task, write_all_time_leaders_summary_task],
        verbose=False
    )

def main():
    user_prompt = input("What would you like to know about the NBA? ")
    default_date = datetime.now().date() - timedelta(1)

    route = route_prompt(user_prompt)

    if route == 'player_stats':
        crew = create_player_stats_crew()
        result = crew.kickoff(inputs={"user_prompt": user_prompt})
        print("Result:")
        parts = str(result).split('---')
        if len(parts) > 1:
            print("Raw Data:")
            print(parts[0].strip())
            print("\nHuman-Readable Summary:")
            print(parts[1].strip())
        else:
            print(result)
    else:  # game_info
        crew = create_game_info_crew()
        result = crew.kickoff(inputs={"user_prompt": user_prompt, "default_date": str(default_date)})
        print("Result:")
        print(result)

if __name__ == "__main__":
    main()