import streamlit as st
import pandas as pd

st.set_page_config(page_title="IPL Fantasy Dashboard", layout="wide")

# ----------------------
# SESSION STATE
# ----------------------
if "teams" not in st.session_state:
    st.session_state.teams = {
        "Ankit": [],
        "Raghav": [],
        "Harsh": [],
        "Daksh": [],
        "Mukund": [],
        "Kundan": [],
        "Vansh": [],
        "Pryam & Nikunj": []
    }

if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------
# POINT SYSTEM
# ----------------------
def batting_points(runs, fours, sixes, balls):
    pts = runs + (fours * 4) + (sixes * 6)

    if runs >= 50:
        pts += 8
    elif runs >= 30:
        pts += 4

    if balls >= 10:
        sr = (runs / balls) * 100
        if sr >= 170:
            pts += 6
        elif sr >= 150:
            pts += 4
        elif sr >= 130:
            pts += 2
        elif sr < 50:
            pts -= 6
        elif sr < 60:
            pts -= 4
        elif sr < 70:
            pts -= 2

    return pts


def bowling_points(wickets, economy):
    pts = wickets * 25

    if wickets >= 3:
        pts += 4

    if economy >= 12:
        pts -= 6
    elif economy >= 11:
        pts -= 4
    elif economy >= 10:
        pts -= 2

    return pts

# ----------------------
# NAVIGATION
# ----------------------
st.sidebar.title("Fantasy Dashboard")
page = st.sidebar.radio("Go to", ["Upload Match", "Teams", "Leaderboard", "History"])

# ----------------------
# UPLOAD MATCH
# ----------------------
if page == "Upload Match":
    st.title("Match Input")

    player = st.text_input("Player Name")
    runs = st.number_input("Runs", 0)
    balls = st.number_input("Balls", 0)
    fours = st.number_input("4s", 0)
    sixes = st.number_input("6s", 0)
    wickets = st.number_input("Wickets", 0)
    economy = st.number_input("Economy", 0.0)
    catches = st.number_input("Catches", 0)

    if st.button("Calculate Points"):
        bat = batting_points(runs, fours, sixes, balls)
        bowl = bowling_points(wickets, economy)
        field = catches * 8

        total = bat + bowl + field

        st.success(f"Total Points: {total}")

# ----------------------
# TEAMS
# ----------------------
elif page == "Teams":
    st.title("Teams")

    tabs = st.tabs(list(st.session_state.teams.keys()))

    for i, team in enumerate(st.session_state.teams):
        with tabs[i]:
            st.subheader(team)

            new_player = st.text_input(f"Add player to {team}", key=team)

            if st.button(f"Add {team}"):
                if new_player:
                    st.session_state.teams[team].append(new_player)

            for p in st.session_state.teams[team]:
                col1, col2 = st.columns([3,1])
                col1.write(p)
                if col2.button("❌", key=p+team):
                    st.session_state.teams[team].remove(p)

# ----------------------
# LEADERBOARD
# ----------------------
elif page == "Leaderboard":
    st.title("Leaderboard")
    st.info("Will update after match integration")

# ----------------------
# HISTORY
# ----------------------
elif page == "History":
    st.title("History")

    for m in st.session_state.history:
        st.write(m)