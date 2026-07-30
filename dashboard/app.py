import streamlit as st

st.set_page_config(
    page_title="Fifa World Cup Analytics",
    page_icon=":material/account_circle:",
    layout="wide",
)

pages = {
    "Dashboard": [
        st.Page(
            "views/homepage.py",
            title="Home",
            icon="📊",
            default=True,
        ),
        st.Page("views/teams.py", title="Teams", icon="🌎"),
        st.Page("views/players.py", title="Players", icon="🏃🏻‍♂️"),
        st.Page("views/predictions.py", title="Predictions", icon="🤖"),
    ]
}

# Navigation Setup
pg = st.navigation(pages, position="top")

# Run Navigation
pg.run()
