import duckdb
import plotly.express as px
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
    order by goals desc
    """
).fetchdf()

st.dataframe(df)
