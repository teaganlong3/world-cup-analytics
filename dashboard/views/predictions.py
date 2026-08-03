import duckdb
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.title("Game Predictions")

# Connect to the local database
conn = duckdb.connect("database/worldcup.duckdb")

# Fetching match data from the database and loading into a dataframe
match_df = conn.execute(
    """
    select *
    from matches
    """
).fetchdf()


# Function to determine the result of a match based on the scores
def get_result(row):
    if row["home_score"] > row["away_score"]:
        return "home_team Win"
    elif row["home_score"] < row["away_score"]:
        return "away_team Win"
    else:
        return "Draw"


# Getting the result of each match based on the scores and adding it as a new column in the match dataframe
match_df["result"] = match_df.apply(get_result, axis=1)

home = match_df[
    [
        "home_team",
        "home_score",
        "home_possession",
        "home_total_shots",
        "home_sot",
        "home_saves",
        "home_corners",
        "home_crosses",
        "home_interceptions",
        "home_fouls",
    ]
]

home.columns = [
    "team",
    "goals",
    "possession",
    "shots",
    "shots_on_target",
    "saves",
    "corners",
    "crosses",
    "interceptions",
    "fouls",
]

away = match_df[
    [
        "away_team",
        "away_score",
        "away_possession",
        "away_total_shots",
        "away_sot",
        "away_saves",
        "away_corners",
        "away_crosses",
        "away_interceptions",
        "away_fouls",
    ]
]

away.columns = home.columns

team_matches = pd.concat([home, away], ignore_index=True)

team_stats = team_matches.groupby("team").mean().reset_index()


matches = match_df.merge(
    team_stats, left_on="home_team", right_on="team", suffixes=("", "_home_avg")
)

matches = matches.drop(columns="team")

matches = matches.rename(
    columns={
        "goals": "home_avg_goals",
        "possession": "home_avg_possession",
        "shots": "home_avg_shots",
        "sot": "home_avg_shots_on_target",
        "saves": "home_avg_saves",
        "corners": "home_avg_corners",
        "crosses": "home_avg_crosses",
        "interceptions": "home_avg_interceptions",
        "fouls": "home_avg_fouls",
    }
)

matches = matches.merge(
    team_stats, left_on="away_team", right_on="team", suffixes=("", "_away_avg")
)

matches = matches.drop(columns="team")

matches = matches.rename(
    columns={
        "goals": "away_avg_goals",
        "possession": "away_avg_possession",
        "shots": "away_avg_shots",
        "sot": "away_avg_shots_on_target",
        "saves": "away_avg_saves",
        "corners": "away_avg_corners",
        "crosses": "away_avg_crosses",
        "interceptions": "away_avg_interceptions",
        "fouls": "away_avg_fouls",
    }
)


matches["goals_difference"] = matches["home_avg_goals"] - matches["away_avg_goals"]
matches["possession_difference"] = (
    matches["home_avg_possession"] - matches["away_avg_possession"]
)
matches["shots_difference"] = matches["home_avg_shots"] - matches["away_avg_shots"]
matches["saves_difference"] = matches["home_avg_saves"] - matches["away_avg_saves"]
matches["crosses_difference"] = (
    matches["home_avg_crosses"] - matches["away_avg_crosses"]
)
matches["interceptions_difference"] = (
    matches["home_avg_interceptions"] - matches["away_avg_interceptions"]
)
matches["fouls_difference"] = matches["home_avg_fouls"] - matches["away_avg_fouls"]


feature_cols = [
    "goals_difference",
    "shots_difference",
    "possession_difference",
    "saves_difference",
    "fouls_difference",
]

x = matches[feature_cols]
y = matches["result"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=500, max_depth=10, min_samples_leaf=3, random_state=42
)

rf.fit(x_train, y_train)

predictions = rf.predict(x_test)

# print(classification_report(y_test, predictions))

team1 = st.selectbox(
    "Home Team:", options=team_stats["team"].unique(), key="team1", index=0
)
team2 = st.selectbox(
    "Away Team:", options=team_stats["team"].unique(), key="team2", index=1
)

if team1 and team2:
    team1_data = team_stats[team_stats["team"].str.contains(team1, case=False)]
    team2_data = team_stats[team_stats["team"].str.contains(team2, case=False)]

    team_stats = team_stats.set_index("team")

    home_stats = team_stats.loc[team1]
    away_stats = team_stats.loc[team2]

    labels = {
        "home_team Win": f"{team1} Win",
        "away_team Win": f"{team2} Win",
        "Draw": "Draw",
    }

    new_match = pd.DataFrame(
        {
            "goals_difference": [home_stats["goals"] - away_stats["goals"]],
            "shots_difference": [home_stats["shots"] - away_stats["shots"]],
            "possession_difference": [
                home_stats["possession"] - away_stats["possession"]
            ],
            "saves_difference": [home_stats["saves"] - away_stats["saves"]],
            "fouls_difference": [home_stats["fouls"] - away_stats["fouls"]],
        }
    )

    probabilities = rf.predict_proba(new_match)[0]

    results = sorted(zip(rf.classes_, probabilities), key=lambda x: x[1], reverse=True)

    st.write(f"**{team1} Vs. {team2} Predictions**")
    cols = st.columns(len(results))

    for col, (label, probability) in zip(cols, results):
        # st.write(f"{labels[label]}: {probability:.2%}")
        with col:
            st.metric(label=labels[label], value=f"{probability:.2%}")
        # st.markdown(f"""{labels[label]}: {probability:.2%}""")
