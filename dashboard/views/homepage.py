import duckdb
import plotly.express as px
import streamlit as st

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

st.markdown(
    """
            <style>
            /* Metric Card Container */
            [data-testid="stMetric"] {
                background-color: #f2f2f2;
                border: 1px solid #d1d5db;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.88);
                width: 100%;
                text-align: center;
            }
            
            /* Metric Title */
            [data-testid="stMetricValue"] {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                font-size: 1.2rem !important;
                font-weight: bold !important;
                color: #374151 !important;
                text-align: center !important;
                white-space: normal !important;
                overflow-wrap: break-word !important;
            }
            
            /* Metric Value */
            [data-testid="stMetricLabel"] {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                font-size: 2rem !important;
                font-weight: bold !important;
                color: #111827 !important;
                text-align: center !important;
                white-space: normal !important;
                overflow-wrap: break-word !important;
            }
            
            /* Remove Default Spacing */
            [data-testid="stMetricDelta"] {
                justify-content: center;
            }
            </style>
            """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.5, 1.5])
col1.metric("⚽ Goals Scored", int(df1["home_score"].sum() + df1["away_score"].sum()))
col2.metric("🥅 Matches Played", df1.shape[0])
col3.metric(
    "🥇 Top Scoring Team", df1.groupby("home_team")["home_score"].sum().idxmax()
)
col4.metric("🏆Golden Boot Winner", df2.groupby("player")["goals"].sum().idxmax())
