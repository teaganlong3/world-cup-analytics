import duckdb
import streamlit as st


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("dashboard/assets/styles.css")

st.title("🏆 World Cup Analytics Dashboard")

st.write(
    """
    This application is an end-to-end sports analytics platform using SQL 
    and Python to process historical World Cup data, create analytical datasets, and 
    visualize team/player performance metrics through interactive dashboards.
    """
)

conn = duckdb.connect("database/worldcup.duckdb")

df1 = conn.execute(
    """
    select *
    from matches
    order by round asc
    """
).fetchdf()

df2 = conn.execute(
    """
    select *
    from players
    """
).fetchdf()

col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.5, 1.5])
col1.metric("⚽ Goals Scored", int(df1["home_score"].sum() + df1["away_score"].sum()))
col2.metric("🥅 Matches Played", df1.shape[0])
col3.metric(
    "🥇 Top Scoring Team", df1.groupby("home_team")["home_score"].sum().idxmax()
)
col4.metric("🏆Golden Boot Winner", df2.groupby("player")["goals"].sum().idxmax())
