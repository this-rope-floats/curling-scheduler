import csv

def export_schedule_csv(schedule, team_names, file_obj):
    writer = csv.writer(file_obj)
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

def export_schedule_html(schedule, team_names, file_obj):
    file_obj.write("<html><head><title>Curling Schedule</title></head><body>")
    file_obj.write("<h1>🏁 Curling Schedule</h1>")

    for week_index, week_data in enumerate(schedule):
        file_obj.write(f"<h2>📅 Week {week_index + 1}</h2>")
        weekly_draws = week_data["draws"]
        bye_teams = [team_names[t] for t in week_data["byes"]]

        for draw_index, draw in enumerate(weekly_draws):
            file_obj.write(f"<h3>Draw {draw_index + 1}</h3><ul>")
            for sheet_num, match in enumerate(draw, start=1):
                if match:
                    a, b = match
                    file_obj.write(f"<li>Sheet {sheet_num}: {team_names[a]} vs {team_names[b]}</li>")
                else:
                    file_obj.write(f"<li>Sheet {sheet_num}: (no game)</li>")
            file_obj.write("</ul>")
        if bye_teams:
            file_obj.write(f"<p><strong>🛋️ Bye Teams:</strong> {', '.join(bye_teams)}</p>")
        else:
            file_obj.write("<p><strong>🛋️ Bye Teams:</strong> None</p>")

    file_obj.write("</body></html>")

def export_player_schedules_csv(schedule, team_rosters, team_names, file_obj):
    from collections import defaultdict
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

    writer = csv.writer(file_obj)
    writer.writerow(["Player", "Week", "Draw", "Sheet", "Opponent", "Status"])
    for player in sorted(player_schedules):
        for entry in player_schedules[player]:
            writer.writerow([player] + entry)

def export_player_schedules_html(schedule, team_rosters, team_names, file_obj):
    from collections import defaultdict
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

    file_obj.write("<html><head><title>Player Schedules</title></head><body>")
    file_obj.write("<h1>📄 Individual Player Schedules</h1>")
    for player in sorted(player_schedules):
        file_obj.write(f"<h2>👤 {player}</h2><ul>")
        for entry in player_schedules[player]:
            file_obj.write(f"<li>{entry}</li>")
        file_obj.write("</ul>")
    file_obj.write("</body></html>")
