import duckdb
import streamlit as st

st.title("Player Analytics")

conn = duckdb.connect("database/worldcup.duckdb")

df = conn.execute(
    """
    select
    team,
    player,
    age,
    goals,
    assists
    from players
    order by player asc
    """
).fetchdf()


st.dataframe(df)
