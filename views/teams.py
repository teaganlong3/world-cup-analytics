import duckdb
import plotly.express as px
import streamlit as st

st.title("Team Analytics")

conn = duckdb.connect("database/worldcup.duckdb")

df = conn.execute(
    """
    select
    home_team_initials,
    sum(home_team_goals) as goals,
    from matches
    group by home_team_initials
    order by goals desc
    """
).fetchdf()

fig = px.bar(df, x="home_team_initials", y="goals")

st.plotly_chart(fig)
