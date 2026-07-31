import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from st_keyup import st_keyup

st.title("Player Analytics")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("dashboard/assets/styles.css")

conn = duckdb.connect("database/worldcup.duckdb")

df = conn.execute(
    """
    select *
    from players
    order by goals desc
    """
).fetchdf()

search = st_keyup("Search players:", key="search_query")

if search:
    result = df[df["player"].str.contains(search, case=False)]

    st.write(f"Found {len(result)} players matching '{search}':")
    st.dataframe(result, hide_index=True)
else:
    st.write("No player name provided. Displaying all players:")
    st.dataframe(df, hide_index=True)


metrics = st.text_input("Enter player name to view metrics:", key="metrics")

if metrics:
    player_data = df[df["player"].str.contains(metrics, case=False)]

    if not player_data.empty:
        bio_col, stat_col = st.columns([1, 2])

        with bio_col:
            st.subheader("Player Bio")
            st.markdown(f"Name: {player_data.iloc[0]['player']}")
            st.markdown(f"Country: {player_data.iloc[0]['team_country']}")
            st.markdown(f"Club: {player_data.iloc[0]['club']}")
            st.markdown(f"Position: {player_data.iloc[0]['position']}")
            st.markdown(f"Age: {player_data.iloc[0]['age']}")
            st.markdown(f"Birth Year: {player_data.iloc[0]['birth_year']}")

        with stat_col:
            st.subheader("Player Analytics")
            mcol1, mcol2 = st.columns(2)
            with mcol1:
                with st.container():
                    st.metric(label="Goals", value=int(player_data["goals"]))
                with st.container():
                    st.metric(label="Shots", value=int(player_data["shots"]))
                with st.container():
                    st.metric(
                        label="Yellow Cards", value=int(player_data["cards_yellow"])
                    )
            with mcol2:
                with st.container():
                    st.metric(label="Passes", value=int(player_data["crosses"]))
                with st.container():
                    st.metric(label="Fouls", value=int(player_data["fouls"]))
                with st.container():
                    st.metric(label="Red Cards", value=int(player_data["cards_red"]))

    else:
        st.write(f"No data found for player '{metrics}'.")
