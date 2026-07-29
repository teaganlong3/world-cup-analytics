import duckdb
import streamlit as st

st.title("Team Analytics")

conn = duckdb.connect("database/worldcup.duckdb")

df = conn.execute(
    """
    select
    team,
    shots,
    goals,
    assists,
    cards_yellow,
    cards_red
    from teams
    order by team asc
    """
).fetchdf()

st.dataframe(df)
