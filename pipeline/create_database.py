import duckdb
import pandas as pd

# Connect to the database (Creates if doesn't exist)
conn = duckdb.connect("database/worldcup.duckdb")

# Loading the CSVs
matches = pd.read_csv("data/WorldCupMatches.csv")
players = pd.read_csv("data/WorldCupPlayers.csv")
worldcups = pd.read_csv("data/WorldCups.csv")

# Cleaning
matches.columns = matches.columns.str.strip().str.lower().str.replace(" ", "_")
players.columns = players.columns.str.strip().str.lower().str.replace(" ", "_")
worldcups.columns = worldcups.columns.str.strip().str.lower().str.replace(" ", "_")

# Creating the tables
conn.register("matches_df", matches)
conn.register("players_df", players)
conn.register("worldcups_df", worldcups)

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
    create or replace table worldcups as
    select * from worldcups_df
    """
)

print("Database created successfully!")
