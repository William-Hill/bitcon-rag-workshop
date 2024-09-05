from crewai import Task

def create_get_all_time_leaders_task(agent):
    return Task(
        description='''
        Analyze the user prompt to determine which NBA statistical category they're interested in.
        Use the get_nba_all_time_leaders tool to find this information.
        The user may ask about leaders in points, assists, rebounds, steals, blocks, field goal percentage, free throw percentage, or three-point percentage.
        Return the top 10 players by default, unless the user specifies a different number.
        User prompt: {user_prompt}
        ''',
        expected_output='A list of all-time leaders for the specified NBA statistical category',
        agent=agent
    )

def create_write_all_time_leaders_summary_task(agent, get_all_time_leaders_task):
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
        agent=agent,
        dependencies=[get_all_time_leaders_task],
        context=[get_all_time_leaders_task]
    )