import streamlit as st
from curling_scheduler import generate_schedule, get_team_rosters, export_schedule_csv, export_schedule_html, export_player_schedules_csv, export_player_schedules_html

st.set_page_config(page_title="Galt Curling Scheduler", layout="wide")

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
    team_rosters, team_names, _ = get_team_rosters(num_teams, team_rosters_input)
    schedule, bye_counts = generate_schedule(num_teams, num_weeks, draws_per_week, num_sheets)

    st.success("✅ Schedule generated!")

    # 📅 Weekly Schedule
    st.header("Weekly Schedule")
    for week_index, week_data in enumerate(schedule):
        st.subheader(f"Week {week_index + 1}")
        for draw_index, draw in enumerate(week_data["draws"]):
            st.markdown(f"**Draw {draw_index + 1}**")
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    st.write(f"Sheet {sheet_num}: {team_names[a]} vs {team_names[b]}")
                else:
                    st.write(f"Sheet {sheet_num}: (no game)")
        if week_data["byes"]:
            st.write("🛋️ Bye Teams:", ", ".join(team_names[t] for t in week_data["byes"]))
        else:
            st.write("🛋️ Bye Teams: None")

    # 📤 Export Options
    st.header("Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Schedule CSV"):
            export_schedule_csv(schedule, team_names)
            st.success("Schedule CSV exported!")
        if st.button("Export Schedule HTML"):
            export_schedule_html(schedule, team_names)
            st.success("Schedule HTML exported!")
    with col2:
        if st.button("Export Player Schedules CSV"):
            export_player_schedules_csv(schedule, team_rosters, team_names)
            st.success("Player CSV exported!")
        if st.button("Export Player Schedules HTML"):
            export_player_schedules_html(schedule, team_rosters, team_names)
            st.success("Player HTML exported!")
