import streamlit as st
from curling_scheduler import generate_schedule, export_schedule_csv, export_schedule_html, export_player_schedules_csv, export_player_schedules_html

st.title("🏁 Curling Scheduler")

# Basic inputs
num_teams = st.number_input("Number of Teams", min_value=2, max_value=20, value=4)
num_weeks = st.number_input("Number of Weeks", min_value=1, max_value=20, value=6)
draws_per_week = st.number_input("Draws per Week", min_value=1, max_value=5, value=2)

# Team roster input
st.header("📋 Team Rosters")
team_rosters_input = {}
team_names = {}
for i in range(1, num_teams + 1):
    st.subheader(f"Team {i}")
    skip = st.text_input(f"Skip (Team {i})", key=f"skip_{i}")
    vice = st.text_input(f"Vice (Team {i})", key=f"vice_{i}")
    second = st.text_input(f"Second (Team {i})", key=f"second_{i}")
    lead = st.text_input(f"Lead (Team {i})", key=f"lead_{i}")
    if skip and vice and second and lead:
        team_rosters_input[i] = [skip, vice, second, lead]
        team_names[i] = f"Team {skip.split()[-1]}"

# Generate button
if st.button("Generate Schedule") and len(team_rosters_input) == num_teams:
    schedule, bye_counts = generate_schedule(num_teams, num_weeks, draws_per_week)

    st.success("✅ Schedule generated!")

    # Display schedule
    st.header("📅 Weekly Schedule")
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

    # Export buttons
    st.header("📤 Export Options")
    if st.button("Export Schedule CSV"):
        export_schedule_csv(schedule, team_names)
        st.success("Schedule CSV exported!")

    if st.button("Export Player Schedules CSV"):
        export_player_schedules_csv(schedule, team_rosters_input, team_names)
        st.success("Player CSV exported!")
