import duckdb
import streamlit as st

st.title("Team Analytics")

# Connect to the local database
conn = duckdb.connect("database/worldcup.duckdb")

# Fetching team and match data from the database and loading into dataframes
df = conn.execute(
    """
    select *
    from teams
    order by team asc
    """
).fetchdf()

st.dataframe(df)
