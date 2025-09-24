import random
from collections import defaultdict
import csv

def get_team_rosters(num_teams, team_rosters_input):
    team_rosters = {}
    player_to_team = {}
    team_names = {}

    for i in range(1, num_teams + 1):
        skip, vice, second, lead = team_rosters_input[i]
        team_name = f"Team {skip.split()[-1]}"
        team_rosters[i] = [skip, vice, second, lead]
        team_names[i] = team_name

        for player in [skip, vice, second, lead]:
            player_to_team[player] = i

    return team_rosters, team_names, player_to_team

def generate_schedule(num_teams, num_weeks, draws_per_week, num_sheets):
    teams = list(range(1, num_teams + 1))
    schedule = []
    opponents = defaultdict(set)
    bye_counts = defaultdict(int)
    draw_distribution = {team: [0] * draws_per_week for team in teams}

    for week in range(num_weeks):
        weekly_draws = [[] for _ in range(draws_per_week)]
        used_teams = set()
        weekly_matchups = []

        possible_matches = []
        for i, a in enumerate(teams):
            for b in teams[i+1:]:
                if a not in used_teams and b not in used_teams:
                    freshness = 0 if b in opponents[a] else 1
                    possible_matches.append((freshness, a, b))

        fresh_matches = [m for m in possible_matches if m[0] == 1]
        rematch_matches = [m for m in possible_matches if m[0] == 0]
        random.shuffle(fresh_matches)
        random.shuffle(rematch_matches)
        sorted_matches = fresh_matches + rematch_matches

        for _, a, b in sorted_matches:
            if a not in used_teams and b not in used_teams:
                weekly_matchups.append((a, b))
                used_teams.update([a, b])
                opponents[a].add(b)
                opponents[b].add(a)

        draw_slots = [[] for _ in range(draws_per_week)]
        for match in weekly_matchups:
            a, b = match
            draw_scores = [draw_distribution[a][i] + draw_distribution[b][i] for i in range(draws_per_week)]
            best_draw = draw_scores.index(min(draw_scores))
            if len(draw_slots[best_draw]) < num_sheets:
                draw_slots[best_draw].append(match)
                draw_distribution[a][best_draw] += 1
                draw_distribution[b][best_draw] += 1
            else:
                for i in range(draws_per_week):
                    if len(draw_slots[i]) < num_sheets:
                        draw_slots[i].append(match)
                        draw_distribution[a][i] += 1
                        draw_distribution[b][i] += 1
                        break

        for draw in draw_slots:
            while len(draw) < num_sheets:
                draw.append(None)

        played_teams = set()
        for draw in draw_slots:
            for match in draw:
                if match:
                    played_teams.update(match)
        bye_teams = sorted(list(set(teams) - played_teams))
        for team in bye_teams:
            bye_counts[team] += 1

        schedule.append({
            "draws": draw_slots,
            "byes": bye_teams
        })

    return schedule, bye_counts

def export_schedule_csv(schedule, team_names, filename="curling_schedule.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Week", "Draw", "Sheet", "Team A", "Team B", "Bye Teams"])

        for week_index, week_data in enumerate(schedule):
            weekly_draws = week_data["draws"]
            bye_teams = [team_names[t] for t in week_data["byes"]]

            for draw_index, draw in enumerate(weekly_draws):
                for sheet_num, match in enumerate(draw, start=1):
                    if match:
                        a, b = match
                        writer.writerow([
                            f"Week {week_index + 1}",
                            f"Draw {draw_index + 1}",
                            f"Sheet {sheet_num}",
                            team_names[a],
                            team_names[b],
                            ""
                        ])
                    else:
                        writer.writerow([
                            f"Week {week_index + 1}",
                            f"Draw {draw_index + 1}",
                            f"Sheet {sheet_num}",
                            "(no game)",
                            "",
                            ""
                        ])
            if bye_teams:
                writer.writerow([
                    f"Week {week_index + 1}",
                    "",
                    "",
                    "",
                    "",
                    ", ".join(bye_teams)
                ])

def export_schedule_html(schedule, team_names, filename="curling_schedule.html"):
    with open(filename, mode="w") as file:
        file.write("<html><head><title>Curling Schedule</title></head><body>")
        file.write("<h1>🏁 Curling Schedule</h1>")

        for week_index, week_data in enumerate(schedule):
            file.write(f"<h2>📅 Week {week_index + 1}</h2>")
            weekly_draws = week_data["draws"]
            bye_teams = [team_names[t] for t in week_data["byes"]]

            for draw_index, draw in enumerate(weekly_draws):
                file.write(f"<h3>Draw {draw_index + 1}</h3><ul>")
                for sheet_num, match in enumerate(draw, start=1):
                    if match:
                        a, b = match
                        file.write(f"<li>Sheet {sheet_num}: {team_names[a]} vs {team_names[b]}</li>")
                    else:
                        file.write(f"<li>Sheet {sheet_num}: (no game)</li>")
                file.write("</ul>")
            if bye_teams:
                file.write(f"<p><strong>🛋️ Bye Teams:</strong> {', '.join(bye_teams)}</p>")
            else:
                file.write("<p><strong>🛋️ Bye Teams:</strong> None</p>")

        file.write("</body></html>")

def export_player_schedules_csv(schedule, team_rosters, team_names, filename="player_schedules.csv"):
    player_schedules = defaultdict(list)

    for week_index, week_data in enumerate(schedule):
        weekly_draws = week_data["draws"]
        bye_teams = week_data["byes"]

        for draw_index, draw in enumerate(weekly_draws):
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    for player in team_rosters[a]:
                        player_schedules[player].append([
                            f"Week {week_index + 1}",
                            f"Draw {draw_index + 1}",
                            f"Sheet {sheet_num}",
                            team_names[b],
                            "Game"
                        ])
                    for player in team_rosters[b]:
                        player_schedules[player].append([
                            f"Week {week_index + 1}",
                            f"Draw {draw_index + 1}",
                            f"Sheet {sheet_num}",
                            team_names[a],
                            "Game"
                        ])

        for team in bye_teams:
            for player in team_rosters[team]:
                player_schedules[player].append([
                    f"Week {week_index + 1}",
                    "",
                    "",
                    "",
                    "BYE"
                ])

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Player", "Week", "Draw", "Sheet", "Opponent", "Status"])
        for player in sorted(player_schedules):
            for entry in player_schedules[player]:
                writer.writerow([player] + entry)

def export_player_schedules_html(schedule, team_rosters, team_names, filename="player_schedules.html"):
    player_schedules = defaultdict(list)

    for week_index, week_data in enumerate(schedule):
        weekly_draws = week_data["draws"]
        bye_teams = week_data["byes"]

        for draw_index, draw in enumerate(weekly_draws):
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    for player in team_rosters[a]:
                        player_schedules[player].append(
                            f"Week {week_index + 1}: vs {team_names[b]} on Draw {draw_index + 1}, Sheet {sheet_num}"
                        )
                    for player in team_rosters[b]:
                        player_schedules[player].append(
                            f"Week {week_index + 1}: vs {team_names[a]} on Draw {draw_index + 1}, Sheet {sheet_num}"
                        )

        for team in bye_teams:
            for player in team_rosters[team]:
                player_schedules[player].append(f"Week {week_index + 1}: BYE")

    with open(filename, mode="w") as file:
        file.write("<html><head><title>Player Schedules</title></head><body>")
        file.write("<h1>📄 Individual Player Schedules</h1>")
        for player in sorted(player_schedules):
            file.write(f"<h2>👤 {player}</h2><ul>")
            for entry in player_schedules[player]:
                file.write(f"<li>{entry}</li>")
            file.write("<//ul>")
        file.write("</body></html>")