from crewai import Crew
from agents import create_nba_researcher, create_nba_statistician, create_nba_writer_llama, create_nba_writer_gemma, create_nba_writer_mixtral, create_nba_editor, create_nba_stats_writer
from tasks import create_collect_game_info_task, create_retrieve_player_stats_task, create_write_game_recap_llama_task, create_write_game_recap_gemma_task, create_write_game_recap_mixtral_task, create_edit_game_recap_task, create_get_all_time_leaders_task, create_write_all_time_leaders_summary_task

def create_game_info_crew():
    return Crew(
        agents=[
            create_nba_researcher(),
            create_nba_statistician(),
            create_nba_writer_llama(),
            create_nba_writer_gemma(),
            create_nba_writer_mixtral(),
            create_nba_editor()
        ],
        tasks=[
            create_collect_game_info_task(),
            create_retrieve_player_stats_task(),
            create_write_game_recap_llama_task(),
            create_write_game_recap_gemma_task(),
            create_write_game_recap_mixtral_task(),
            create_edit_game_recap_task()
        ],
        verbose=False
    )

def create_player_stats_crew():
    return Crew(
        agents=[create_nba_researcher(), create_nba_stats_writer()],
        tasks=[create_get_all_time_leaders_task(), create_write_all_time_leaders_summary_task()],
        verbose=False
    )