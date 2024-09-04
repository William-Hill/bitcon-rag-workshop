from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2, alltimeleadersgrids
from nba_api.stats.static import teams
from datetime import datetime, timedelta
import json
from crewai_tools import tool

@tool
def get_nba_game_info(date_str:str, team:str):
    """
    Get information about an NBA game for a specific date and/or team, including the boxscore.

    Args:
    date_str (str, optional): The date of the game in 'YYYY-MM-DD' format. If not provided, defaults to yesterday.
    team (str, optional): The team name or abbreviation to filter games. If not provided, returns games for all teams on the given date.

    Returns:
    str: A JSON string containing game information including game_id, home_team, away_team, scores, date, and boxscore.
    """
    print(f"Date: {date_str}")
    print(f"Team: {team}")
    if date_str:
        game_date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        game_date = datetime.now() - timedelta(days=1)

    # Determine the season based on the game date
    year = game_date.year
    month = game_date.month
    if month >= 10:
        season_year = str(year)
    else:
        season_year = str(year - 1)

    team_id = None
    if team:
        # Get all teams
        nba_teams = teams.get_teams()
        # Find the team (case-insensitive)
        team_found = next((t for t in nba_teams if team.lower() in (t['full_name'].lower(), t['abbreviation'].lower())), None)
        if team_found:
            team_id = team_found['id']
            print(f"Team ID: {team_id}")
        else:
            return json.dumps({"error": f"Team '{team}' not found."}, indent=2)

    # Use leaguegamefinder to get games for the specified team (or all teams if not specified)
    gamefinder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        league_id_nullable='00'
    )
    games = gamefinder.get_data_frames()[0]

    # Filter games for the specific season and date
    games = games[(games.SEASON_ID.str[-4:] == season_year) & (games['GAME_DATE'] == game_date.strftime("%Y-%m-%d"))]

    if games.empty:
        return json.dumps({"error": f"No games found for the specified date {date_str} and team {team}."}, indent=2)

    # Sort games by GAME_ID to ensure consistent ordering
    games = games.sort_values('GAME_ID')
    game = games.iloc[0]

    game_id = str(game['GAME_ID'])
    
    # Get the opponent's information
    opponent_game = games[games['GAME_ID'] == game_id].iloc[1] if len(games) > 1 else None

    # Determine home and away teams
    if game['MATCHUP'].startswith('vs.'):
        home_team = game['TEAM_ABBREVIATION']
        away_team = opponent_game['TEAM_ABBREVIATION'] if opponent_game is not None else "Unknown"
        home_score = game['PTS']
        away_score = opponent_game['PTS'] if opponent_game is not None else 0
    else:
        away_team = game['TEAM_ABBREVIATION']
        home_team = opponent_game['TEAM_ABBREVIATION'] if opponent_game is not None else "Unknown"
        away_score = game['PTS']
        home_score = opponent_game['PTS'] if opponent_game is not None else 0

    # Get boxscore data
    boxscore_data = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    player_stats = boxscore_data.get_data_frames()[0]
    team_stats = boxscore_data.get_data_frames()[1]
    
    game_info = {
        'game_id': game_id,
        'home_team': home_team,
        'away_team': away_team,
        'home_score': int(home_score),
        'away_score': int(away_score),
        'date': game_date.strftime("%Y-%m-%d"),
        'season': game['SEASON_ID'],
        'boxscore': {
            'player_stats': player_stats.to_dict(orient='records'),
            'team_stats': team_stats.to_dict(orient='records')
        }
    }
    
    return json.dumps(game_info, indent=2)

@tool
def get_nba_player_stats(game_id):
    """
    Get player statistics for a specific NBA game.

    Args:
    game_id (str): The ID of the NBA game to retrieve player stats for.

    Returns:
    str: A JSON string containing a list of player statistics including team, name, position, and various game stats.
    """
    box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    player_stats = box_score.get_data_frames()[0]
    
    relevant_stats = player_stats[['TEAM_ABBREVIATION', 'PLAYER_NAME', 'START_POSITION', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'TO', 'PLUS_MINUS']]
    
    stats_list = relevant_stats.to_dict(orient='records')
    return json.dumps(stats_list, indent=2)

# Additional tool to get live game data if needed
@tool
def get_live_game_data(game_date=None):
    """
    Get live game data for NBA games currently in progress.

    Args:
    game_date (str, optional): The date to retrieve live game data for. If not provided, uses the current date.

    Returns:
    str: A JSON string containing a list of live game information including game_id, team names, scores, status, clock, and period.
    """
    live_scoreboard = scoreboard.ScoreBoard()
    games = live_scoreboard.get_dict()['scoreboard']['games']
    
    formatted_games = []
    for game in games:
        formatted_game = {
            'game_id': game['gameId'],
            'home_team': game['homeTeam']['teamTricode'],
            'away_team': game['awayTeam']['teamTricode'],
            'home_score': game['homeTeam']['score'],
            'away_score': game['awayTeam']['score'],
            'status': game['gameStatus'],
            'clock': game['gameClock'],
            'period': game['period']
        }
        formatted_games.append(formatted_game)
    
    return json.dumps(formatted_games, indent=2)

@tool
def get_nba_all_time_leaders(stat_category: str, top_n: int = 10) -> str:
    """
    Get the all-time leaders in a specified NBA statistical category.

    Args:
    stat_category (str): The statistical category to retrieve leaders for. 
                         Valid options include: 'PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FT_PCT', 'FG3_PCT'.
    top_n (int, optional): The number of top players to return. Defaults to 10.

    Returns:
    str: A JSON string containing the top players in the specified statistical category.
    """
    # Map of user-friendly stat names to API method names
    stat_map = {
        'PTS': 'pts_leaders',
        'AST': 'ast_leaders',
        'REB': 'reb_leaders',
        'STL': 'stl_leaders',
        'BLK': 'blk_leaders',
        'FG_PCT': 'fg_pct_leaders',
        'FT_PCT': 'ft_pct_leaders',
        'FG3_PCT': 'fg3_pct_leaders'
    }

    if stat_category not in stat_map:
        return json.dumps({"error": f"Invalid stat category. Valid options are: {', '.join(stat_map.keys())}"}, indent=2)

    # Get the all-time leaders data
    leaders = alltimeleadersgrids.AllTimeLeadersGrids()
    
    # Get the appropriate dataframe
    df = getattr(leaders, stat_map[stat_category]).get_data_frame()

    # Get the top N players (the data is already sorted)
    df_top = df.head(top_n)
    print("df_top:", df_top)

    # Format the results
    results = []
    print("stat_category:", stat_category)
    for _, player in df_top.iterrows():
        print("player:", player.to_dict())
        print("player['stat_category']:", player[stat_category])
        result = {
            'PLAYER_NAME': player['PLAYER_NAME'],
            stat_category: float(player[stat_category]) if stat_category in ['FG_PCT', 'FT_PCT', 'FG3_PCT'] else int(player[stat_category]),
            'RANK': int(player[f'{stat_category}_RANK'])
        }
        if 'TEAM' in player:
            result['TEAM'] = player['TEAM']
        results.append(result)

    return json.dumps(results, indent=2)