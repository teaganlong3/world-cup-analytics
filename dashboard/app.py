import streamlit as st

home_page = st.Page(
    page="views/homepage.py",
    title="Fifa World Cup Analytics",
    icon=":material/account_circle:",
    default=True,
)

player_analytics = st.Page(
    page="views/players.py",
    title="Player Analytics",
    icon=":material/bar_chart:",
)

team_analytics = st.Page(
    page="views/teams.py",
    title="Team Analytics",
    icon=":material/bar_chart:",
)

prediction_model = st.Page(
    page="views/predictions.py",
    title="Game Predictions",
    icon=":material/bar_chart:",
)

# Navigation Setup
pg = st.navigation(
    pages=[home_page, team_analytics, player_analytics, prediction_model]
)

# Run Navigation
pg.run()
