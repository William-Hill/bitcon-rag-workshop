from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2, alltimeleadersgrids
from nba_api.stats.static import teams
from datetime import datetime, timedelta
import json
from crewai_tools import tool

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