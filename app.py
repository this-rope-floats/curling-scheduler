import streamlit as st
import io
import os
from curling_scheduler import (
    generate_schedule,
    get_team_rosters,
    export_schedule_csv,
    export_schedule_html,
    export_player_schedules_csv,
    export_player_schedules_html
)

st.set_page_config(
    page_title="Galt Curling Scheduler",
    page_icon="🥌",
    layout="wide"
)

# 🥌 Logo and Title
st.image("https://raw.githubusercontent.com/this-rope-floats/curling-scheduler/main/galt_logo.png", width=200)
st.title("🏁 Galt Curling Club Scheduler")
st.markdown("Welcome to the official scheduler for the Galt Curling Club! Customize your league setup and generate weekly matchups with ease.")

# 📋 Sidebar Inputs
st.sidebar.header("League Settings")
num_teams = st.sidebar.number_input("Number of Teams", min_value=2, max_value=20, value=4)
num_weeks = st.sidebar.number_input("Number of Weeks", min_value=1, max_value=20, value=6)
draws_per_week = st.sidebar.number_input("Draws per Week", min_value=1, max_value=5, value=2)
num_sheets = st.sidebar.number_input("Sheets per Draw", min_value=1, max_value=8, value=4)

# 🧑‍🤝‍🧑 Team Rosters
st.header("Team Rosters")
team_rosters_input = {}
team_names = {}

for i in range(1, num_teams + 1):
    with st.expander(f"Team {i}"):
        skip = st.text_input(f"Skip (Team {i})", key=f"skip_{i}")
        vice = st.text_input(f"Vice (Team {i})", key=f"vice_{i}")
        second = st.text_input(f"Second (Team {i})", key=f"second_{i}")
        lead = st.text_input(f"Lead (Team {i})", key=f"lead_{i}")
        if skip and vice and second and lead:
            team_rosters_input[i] = [skip, vice, second, lead]
            team_names[i] = f"Team {skip.split()[-1]}"

# 🧮 Generate Schedule
if st.button("Generate Schedule") and len(team_rosters_input) == num_teams:
    team_rosters, team_names, player_to_team = get_team_rosters(num_teams, team_rosters_input)
    schedule, bye_counts = generate_schedule(num_teams, num_weeks, draws_per_week, num_sheets)

    st.success("✅ Schedule generated!")

    # 📅 Weekly Schedule
    st.header("Weekly Schedule")
    draw_distribution = {team: [0] * draws_per_week for team in range(1, num_teams + 1)}
    player_schedules = {}

    for week_index, week_data in enumerate(schedule):
        st.subheader(f"Week {week_index + 1}")
        for draw_index, draw in enumerate(week_data["draws"]):
            st.markdown(f"**Draw {draw_index + 1}**")
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    draw_distribution[a][draw_index] += 1
                    draw_distribution[b][draw_index] += 1
                    st.markdown(
                        f"<span style='color:green'><strong>Sheet {sheet_num}:</strong> {team_names[a]} vs {team_names[b]}</span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f"<span style='color:gray'>Sheet {sheet_num}: (no game)</span>", unsafe_allow_html=True)
        if week_data["byes"]:
            st.markdown(
                f"<span style='color:orange'><strong>🛋️ Bye Teams:</strong> {', '.join(team_names[t] for t in week_data['byes'])}</span>",
                unsafe_allow_html=True
            )
        else:
            st.markdown("<strong>🛋️ Bye Teams:</strong> None", unsafe_allow_html=True)

    # 📊 Fairness Metrics
    st.header("📊 Fairness Metrics")
    for team in range(1, num_teams + 1):
        total_games = sum(draw_distribution[team])
        st.write(f"{team_names[team]}: {total_games} games, {bye_counts[team]} byes")

    # 👤 Player Schedule Viewer
    st.header("👤 Player Schedule Viewer")
    from collections import defaultdict
    player_schedules = defaultdict(list)

    for week_index, week_data in enumerate(schedule):
        for draw_index, draw in enumerate(week_data["draws"]):
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    for player in team_rosters[a]:
                        player_schedules[player].append(f"Week {week_index + 1}: vs {team_names[b]} on Draw {draw_index + 1}, Sheet {sheet_num}")
                    for player in team_rosters[b]:
                        player_schedules[player].append(f"Week {week_index + 1}: vs {team_names[a]} on Draw {draw_index + 1}, Sheet {sheet_num}")
        for team in week_data["byes"]:
            for player in team_rosters[team]:
                player_schedules[player].append(f"Week {week_index + 1}: BYE")

    selected_player = st.selectbox("Select a player to view their schedule:", sorted(player_schedules.keys()))
    st.subheader(f"Schedule for {selected_player}")
    for entry in player_schedules[selected_player]:
        st.write(entry)

    # 📥 Download Buttons
    st.header("📥 Download Schedule Files")

    # Overall Schedule CSV
    export_schedule_csv(schedule, team_names, filename="curling_schedule.csv")
    with open("curling_schedule.csv", "r") as f:
        csv_data = f.read()
    st.download_button("Download Overall Schedule (CSV)", csv_data, file_name="curling_schedule.csv", mime="text/csv")

    # Overall Schedule HTML
    export_schedule_html(schedule, team_names, filename="curling_schedule.html")
    with open("curling_schedule.html", "r") as f:
        html_data = f.read()
    st.download_button("Download Overall Schedule (HTML)", html_data, file_name="curling_schedule.html", mime="text/html")

    # Player Schedules CSV
    export_player_schedules_csv(schedule, team_rosters, team_names, filename="player_schedules.csv")
    with open("player_schedules.csv", "r") as f:
        player_csv_data = f.read()
    st.download_button("Download Player Schedules (CSV)", player_csv_data, file_name="player_schedules.csv", mime="text/csv")

    # Player Schedules HTML
    export_player_schedules_html(schedule, team_rosters, team_names, filename="player_schedules.html")
    with open("player_schedules.html", "r") as f:
        player_html_data = f.read()
    st.download_button("Download Player Schedules (HTML)", player_html_data, file_name="player_schedules.html", mime="text/html")

    # Optional cleanup
    os.remove("curling_schedule.csv")
    os.remove("curling_schedule.html")
    os.remove("player_schedules.csv")
    os.remove("player_schedules.html")

# 📞 Footer
st.markdown("---")
st.markdown("Built by This Rope Floats for the Galt Curling Club 🥌. Questions? Email [curling@thisropefloats.ca](mailto:curling@thisropefloats.ca)")

