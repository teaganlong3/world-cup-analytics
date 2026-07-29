import duckdb
import pandas as pd

# Connect to the database (Creates if doesn't exist)
conn = duckdb.connect("database/worldcup.duckdb")

# Loading the CSVs
matches = pd.read_csv("data/matches.csv")
players = pd.read_csv("data/players.csv")
teams = pd.read_csv("data/teams.csv")

# Cleaning
matches.columns = matches.columns.str.strip().str.lower().str.replace(" ", "_")
players.columns = players.columns.str.strip().str.lower().str.replace(" ", "_")
teams.columns = teams.columns.str.strip().str.lower().str.replace(" ", "_")

# Creating the tables
conn.register("matches_df", matches)
conn.register("players_df", players)
conn.register("teams_df", teams)

conn.execute(
    """
    create or replace table matches as
    select * from matches_df
    """
)

conn.execute(
    """
    create or replace table players as
    select * from players_df
    """
)

conn.execute(
    """
    create or replace table teams as
    select * from teams_df
    """
)

print("Database created successfully!")
