import os
import statsapi
import datetime
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

@tool
def get_game_info(game_date: str, team_name: str) -> str:
    """Gets high-level information on an MLB game.
    
    Params:
    game_date: The date of the game of interest, in the form "yyyy-mm-dd". 
    team_name: MLB team name. Both full name (e.g. "New York Yankees") or nickname ("Yankees") are valid. If multiple teams are mentioned, use the first one
    """
    print(f"Game Date: {game_date}")
    print(f"Team Name: {team_name}")
    sched = statsapi.schedule(start_date=game_date,end_date=game_date)
    sched_df = pd.DataFrame(sched)
    game_info_df = sched_df[sched_df['summary'].str.contains(team_name, case=False, na=False)]
    if game_info_df.empty:
        return "No game found for team {team_name} on {game_date}."
    else:
        print("game_info_df:", game_info_df)
        
    game_id = str(game_info_df.game_id.tolist()[0])
    home_team = game_info_df.home_name.tolist()[0]
    home_score = game_info_df.home_score.tolist()[0]
    away_team = game_info_df.away_name.tolist()[0]
    away_score = game_info_df.away_score.tolist()[0]
    winning_team = game_info_df.winning_team.tolist()[0]
    series_status = game_info_df.series_status.tolist()[0]

    game_info = '''
        Game ID: {game_id}
        Home Team: {home_team}
        Home Score: {home_score}
        Away Team: {away_team}
        Away Score: {away_score}
        Winning Team: {winning_team}
        Series Status: {series_status}
    '''.format(game_id = game_id, home_team = home_team, home_score = home_score, 
               away_team = away_team, away_score = away_score, \
                series_status = series_status, winning_team = winning_team)

    return game_info


@tool 
def get_batting_stats(game_id: str) -> str:
    """Gets player boxscore batting stats for a particular MLB game
    
    Params:
    game_id: The 6-digit ID of the game
    """
    boxscores=statsapi.boxscore_data(game_id)
    player_info_df = pd.DataFrame(boxscores['playerInfo']).T.reset_index()

    away_batters_box = pd.DataFrame(boxscores['awayBatters']).iloc[1:]
    away_batters_box['team_name'] = boxscores['teamInfo']['away']['teamName']

    home_batters_box = pd.DataFrame(boxscores['homeBatters']).iloc[1:]
    home_batters_box['team_name'] = boxscores['teamInfo']['home']['teamName']

    batters_box_df = pd.concat([away_batters_box, home_batters_box]).merge(player_info_df, left_on = 'name', right_on = 'boxscoreName')
    return str(batters_box_df[['team_name','fullName','position','ab','r','h','hr','rbi','bb','sb']])


@tool 
def get_pitching_stats(game_id: str) -> str:
    """Gets player boxscore pitching stats for a particular MLB game
    
    Params:
    game_id: The 6-digit ID of the game
    """
    boxscores=statsapi.boxscore_data(game_id)
    player_info_df = pd.DataFrame(boxscores['playerInfo']).T.reset_index()

    away_pitchers_box = pd.DataFrame(boxscores['awayPitchers']).iloc[1:]
    away_pitchers_box['team_name'] = boxscores['teamInfo']['away']['teamName']

    home_pitchers_box = pd.DataFrame(boxscores['homePitchers']).iloc[1:]
    home_pitchers_box['team_name'] = boxscores['teamInfo']['home']['teamName']

    pitchers_box_df = pd.concat([away_pitchers_box,home_pitchers_box]).merge(player_info_df, left_on = 'name', right_on = 'boxscoreName')
    return str(pitchers_box_df[['team_name','fullName','ip','h','r','er','bb','k','note']])
