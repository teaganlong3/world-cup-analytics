import duckdb
import streamlit as st

st.title("Player Analytics")

conn = duckdb.connect("database/worldcup.duckdb")

df = conn.execute(
    """
    select
    team_initials,
    player_name,
    from players
    order by team_initials asc
    """
).fetchdf()

team = st.sidebar.text_input("Enter a Team's Initials")

filtered_df = df.query("team_initials == @team")

st.dataframe(filtered_df)
