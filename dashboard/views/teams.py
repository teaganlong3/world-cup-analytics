import duckdb
import streamlit as st
from st_keyup import st_keyup

st.title("Team Analytics")

# Connect to the local database
conn = duckdb.connect("database/worldcup.duckdb")

# Fetching team data from the database and loading into a dataframe
team_df = conn.execute(
    """
    select *
    from teams
    order by team asc
    """
).fetchdf()

# Fetching match data from the database and loading into a dataframe
match_df = conn.execute(
    """
    select *
    from matches
    """
).fetchdf()

# Continuous search functionality for teams using st_keyup
# The search input field allows users to type a team's name and dynamically filter the displayed results in real-time.
# If a search is not provided, all teams are displayed by default.
search = st_keyup("Search teams:", key="search_query")

if search:
    result = team_df[team_df["team"].str.contains(search, case=False)]

    st.write(f"Found {len(result)} teams matching '{search}':")
    st.dataframe(
        result[["team", "games", "minutes", "goals", "assists", "possession"]],
        hide_index=True,
    )
else:
    st.write("No team name provided. Displaying leaderboard")
    leaderboard = match_df[::-1][["round", "home_team", "away_team", "score"]]
    st.dataframe(leaderboard, hide_index=True)

# Team comparison feature allowing users to select two teams and compare their performance metrics side by side
team1 = st.selectbox(
    "Select Team 1:", options=team_df["team"].unique(), key="team1", index=0
)
team2 = st.selectbox(
    "Select Team 2:", options=team_df["team"].unique(), key="team2", index=1
)

if team1 and team2:
    team1_data = team_df[team_df["team"].str.contains(team1, case=False)]
    team2_data = team_df[team_df["team"].str.contains(team2, case=False)]

    st.subheader(f"Comparison: {team1} vs {team2}")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{team1} Performance Metrics:**")
        st.markdown(
            f"""
            - Games Played: {team1_data.iloc[0]["games"]}
            - Minutes Played: {team1_data.iloc[0]["minutes"]}
            - Goals Scored: {team1_data.iloc[0]["goals"]}
            - Assists: {team1_data.iloc[0]["assists"]}
            - Possession: {team1_data.iloc[0]["possession"]}%
            """
        )
    with col2:
        st.write(f"**{team2} Performance Metrics:**")
        st.markdown(
            f"""
            - Games Played: {team2_data.iloc[0]["games"]}
            - Minutes Played: {team2_data.iloc[0]["minutes"]}
            - Goals Scored: {team2_data.iloc[0]["goals"]}
            - Assists: {team2_data.iloc[0]["assists"]}
            - Possession: {team2_data.iloc[0]["possession"]}%
            """
        )

    # Displaying the game history for both teams side by side, allowing users to see past matchups and results
    st.write("Game History Comparison:")
    col_1, col2 = st.columns(2)
    with col_1:
        st.write(f"**{team1}:**")
        team1_history = match_df[
            (match_df["home_team"].str.contains(team1, case=False))
            | (match_df["away_team"].str.contains(team1, case=False))
        ]
        st.dataframe(
            team1_history[["round", "home_team", "away_team", "score"]],
            hide_index=True,
        )
    with col2:
        st.write(f"**{team2}:**")
        team2_history = match_df[
            (match_df["home_team"].str.contains(team2, case=False))
            | (match_df["away_team"].str.contains(team2, case=False))
        ]
        st.dataframe(
            team2_history[["round", "home_team", "away_team", "score"]],
            hide_index=True,
        )
else:
    st.write("Please select both teams to compare their performance metrics.")
