from datetime import datetime, timedelta
from crewai import Crew
from agents import create_nba_researcher, create_nba_stats_writer
from tasks import create_get_all_time_leaders_task, create_write_all_time_leaders_summary_task

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
    user_prompt = input("What would you like to know about NBA all-time leaders? ")

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

if __name__ == "__main__":
    main()