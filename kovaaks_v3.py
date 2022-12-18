import os, json, csv, webbrowser, datetime


path_kovaaks = r"C:\Spiele\SteamLibrary\steamapps\common\FPSAimTrainer"
path_stats = os.path.join(path_kovaaks, "FPSAimTrainer", "stats")
path_playlists = os.path.join(path_kovaaks, "FPSAimTrainer", "Saved", "SaveGames", "Playlists")


playlist_name = input("Playlist Name: ").strip("\t\n\r") + ".json" 
day = input("Date (DD.MM.YYYY): ").strip("\t\n\r")

if day:
    day = datetime.datetime.strptime(day, "%d.%m.%Y")
else:
    day = datetime.datetime.today()

day_1 = day + datetime.timedelta(days=1)
day = day.strftime("%Y.%m.%d")
day_1 = day_1.strftime("%Y.%m.%d")


with open(os.path.join(path_playlists, playlist_name)) as json_file:
    playlist_json = json.load(json_file)
    scenarios_playlist = [playlist_json["scenarioList"][idx]["scenario_Name"].lower() for idx, _ in enumerate(playlist_json["scenarioList"])]


filenames = []
for file in os.listdir(path_stats):
    if any(scen_name in file.lower() for scen_name in scenarios_playlist):
        filenames.append(file)


scenario_dates = [filename.split(" - ")[-1].split("-")[0] for filename in filenames]
scenario_names = []
scenario_scores = []

for filename in filenames:
    with open(os.path.join(path_stats, filename)) as file:
        scenario_lines = file.read().splitlines()

        scenario_name = scenario_lines[-23].split(":,")[-1].lower()
        scenario_score = float(scenario_lines[-24].split(":,")[-1])
        
        scenario_names.append(scenario_name)
        scenario_scores.append(scenario_score)


names_scores = {}
for name, date_score in zip(scenario_names, zip(scenario_dates, scenario_scores)):
    if name in names_scores:
        names_scores[name].append(date_score)
    else:
        names_scores[name] = [date_score]


playlist_stats = []
for scenario in scenarios_playlist:
    name_score_list = names_scores[scenario]
    scores = []
    for date, score in name_score_list:
        if date == day or date == day_1:
            scores.append(score)
    try:
        score_max = round(max(scores))
        score_avg = round(sum(scores) / len(scores))
    except ValueError:
        score_max = "/"
        score_avg = "/"
    playlist_stats.append((score_max, score_avg))


csv_name = os.path.join("stats", f"{day} - {playlist_name}.txt")
with open(csv_name, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter="\t")
    writer.writerows(playlist_stats)

webbrowser.open(csv_name)