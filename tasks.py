from crewai import Task

def create_collect_game_info_task(nba_researcher):
    return Task(
        description='''
        Identify the correct NBA game related to the user prompt and return game info using the get_nba_game_info tool. 
        Unless a specific date is provided in the user prompt, use {default_date} as the game date.
        If no game is found, inform the user and suggest trying a different date or team.
        User prompt: {user_prompt}
        ''',
        expected_output='High-level information of the relevant NBA game or an error message if no game is found',
        agent=nba_researcher
    )

def create_retrieve_player_stats_task(nba_statistician):
    return Task(
        description='Retrieve ONLY boxscore player stats for the relevant NBA game',
        expected_output='A table of player boxscore stats',
        agent=nba_statistician,
        dependencies=[create_collect_game_info_task],
        context=[create_collect_game_info_task]
    )

def create_write_game_recap_llama_task(nba_writer_llama):
    return Task(
        description='''
        Write a game recap article using the provided NBA game information and stats.
        Key instructions:
        - Include things like final score, top scorers, and key team stats.
        - Use ONLY the provided data and DO NOT make up any information, such as specific quarters when events occurred, that isn't explicitly from the provided input.
        - Do not print the box score
        ''',
        expected_output='An NBA game recap article',
        agent=nba_writer_llama,
        dependencies=[create_collect_game_info_task, create_retrieve_player_stats_task],
        context=[create_collect_game_info_task, create_retrieve_player_stats_task]
    )

def create_write_game_recap_gemma_task(nba_writer_gemma):
    return Task(
        description='''
        Write a game recap article using the provided NBA game information and stats.
        Key instructions:
        - Include things like final score, top scorers, and key team stats.
        - Use ONLY the provided data and DO NOT make up any information, such as specific quarters when events occurred, that isn't explicitly from the provided input.
        - Do not print the box score
        ''',
        expected_output='An NBA game recap article',
        agent=nba_writer_gemma,
        dependencies=[create_collect_game_info_task, create_retrieve_player_stats_task],
        context=[create_collect_game_info_task, create_retrieve_player_stats_task]
    )

def create_write_game_recap_mixtral_task(nba_writer_mixtral):
    return Task(
        description='''
        Write a succinct NBA game recap article using the provided game information and stats.
        Key instructions:
        - Structure with the following sections:
              - Introduction (game result, top scorer, key team stats)
              - Key performers on the winning team
              - Key performers on the losing team
              - Conclusion (including series result if applicable)
        - Use ONLY the provided data and DO NOT make up any information, such as specific quarters when events occurred, that isn't explicitly from the provided input.
        - Do not print the box score or write out the section names
        ''',
        expected_output='An NBA game recap article',
        agent=nba_writer_mixtral,
        dependencies=[create_collect_game_info_task, create_retrieve_player_stats_task],
        context=[create_collect_game_info_task, create_retrieve_player_stats_task]
    )

def create_edit_game_recap_task(nba_editor):
    return Task(
        description='''
        You will be provided three game recap articles from multiple writers. Take the best of
        all three to output the optimal final article.
        
        Pay close attention to the original instructions:

        Key instructions:
            - Structure with the following sections:
              - Introduction (game result, top scorer, key team stats)
              - Key performers on the winning team
              - Key performers on the losing team
              - Conclusion (including series result if applicable)
            - Use ONLY the provided data and DO NOT make up any information, such as specific quarters when events occurred, that isn't explicitly from the provided input.
            - Do not print the box score or write out the section names

        It is especially important that no false information, such as any quarter or the quarter in which an event occurred, 
        is present in the final product. If a piece of information is present in one article and not the others, it is probably false
        ''',
        expected_output='An NBA game recap article',
        agent=nba_editor,
        dependencies=[create_write_game_recap_llama_task, create_write_game_recap_gemma_task, create_write_game_recap_mixtral_task],
        context=[create_collect_game_info_task, create_retrieve_player_stats_task, create_write_game_recap_llama_task, create_write_game_recap_gemma_task, create_write_game_recap_mixtral_task]
    )

def create_get_all_time_leaders_task(nba_researcher):
    return Task(
        description='''
        Analyze the user prompt to determine which NBA statistical category they're interested in.
        Use the get_nba_all_time_leaders tool to find this information.
        The user may ask about leaders in points, assists, rebounds, steals, blocks, field goal percentage, free throw percentage, or three-point percentage.
        Return the top 10 players by default, unless the user specifies a different number.
        User prompt: {user_prompt}
        ''',
        expected_output='A list of all-time leaders for the specified NBA statistical category',
        agent=nba_researcher
    )

def create_write_all_time_leaders_summary_task(nba_stats_writer, get_all_time_leaders_task):
    return Task(
        description='''
        Write a clear, concise summary of the NBA all-time leaders in the specified statistical category.
        Use the data provided by the get_all_time_leaders task.
        Format the information in an easy-to-read, engaging manner.
        Include the player's name, their stat value, and their rank.
        If available, include the team(s) they played for.
        Provide any interesting context or records related to these achievements.
        
        In your response, first include the raw data from get_all_time_leaders, then provide your human-readable summary.
        Separate the two parts with a line of dashes (---).
        ''',
        expected_output='Raw data followed by a human-readable summary of NBA all-time leaders in the specified statistical category',
        agent=nba_stats_writer,
        dependencies=[get_all_time_leaders_task],
        context=[get_all_time_leaders_task]
    )