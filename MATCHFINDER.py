import os
import json
from fuzzywuzzy import fuzz
non_corresponding_matches = []
# Function to find matches between teams in two sets of data
def find_matches(data1, data2):
    matches = []
    # Iterate through each match in the first set of data
    for match1 in data1:
        match_flag = False
        home1 = match1["Home Team"]
        away1 = match1["Away Team"]

        # Iterate through each match in the second set of data
        for match2 in data2:
            home2 = match2["Home Team"]
            away2 = match2["Away Team"]

            
            if (fuzz.ratio(home1, home2) > 85 or fuzz.partial_ratio(home1, home2) > 85) and \
               (fuzz.ratio(away1, away2) > 85 or fuzz.partial_ratio(away1, away2) > 85):
                matches.append((match1, match2))
                match_flag = True
        if(not match_flag):
            non_corresponding_matches.append(match1)
           


    return matches

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Define the folder containing the JSON files
folder_path = "Betdata"

# Take json files from the Betdata folder
json_files = [
    os.path.join(folder_path, file) 
    for file in os.listdir(folder_path) 
    if file.endswith(".json") 
    and file not in ["games.json", "surebetresults.json", "Multipliers.json", "SUREBETS.json"]
]

# Prepare output data
output_data = []
# Preload data from all files and store them along with their file names
preloaded_data = [(os.path.basename(file).split(".")[0], load_json(file)) for file in json_files]
# Initialize an empty list to store the output data
output_data = []

# Iterate through each unique pair of files
for i in range(len(preloaded_data)-1):
    if (i == 0):
        source_name1, data1 = preloaded_data[i]
        source_name2, data2 = preloaded_data[i+1]
    else:
        data1 = output_data
        source_name2, data2 = preloaded_data[i+1]

    # Find matches between the two datasets
    matches = find_matches(data1, data2)
    for match1, match2 in matches:
        home_team = match1["Home Team"]
        away_team = match1["Away Team"]

        # Simplify the process of setting default odds values
        for match in (match1, match2):
            for outcome in ("Home", "Away", "Draw", 'Highest Home Odds', 'Highest Draw Odds', 'Highest Away Odds'):
                try:
                    if not isinstance(match[outcome], float):
                        match[outcome] = 0.9
                except:
                    pass

        # Calculate odds for both matches
        if (i == 0):
            odds1 = {outcome: float(match1[outcome]) for outcome in ("Home", "Draw", "Away")}
        else:
            odds1 = {outcome: float(match1[outcome]) for outcome in ("Highest Home Odds", "Highest Draw Odds", "Highest Away Odds")}        
        odds2 = {outcome: float(match2[outcome]) for outcome in ("Home", "Draw", "Away")}

        # Determine the highest odds and their sources for each outcome
        if(i==0):
            highest_odds = {outcome: max(odds1[outcome], odds2[outcome]) for outcome in odds1}
        else:
            highest_odds = {outcome: max(odds1[outcome], odds2[outcome[8:12]]) for outcome in odds1}
        if (i == 0):
            sources = {outcome: source_name1 if odds1[outcome] >= odds2[outcome] else source_name2 for outcome in odds1}
        else:

            sources = {}  # Initialize sources as an empty dictionary
            for outcome in odds1:
                if odds1[outcome] >= odds2[outcome[8:12]]:
                    sources[outcome] = match1["Source " + outcome[8:12]]
                else:
                    sources[outcome] = source_name2

        # Append the results to the output data list
        if i == 0:
            output_data.append({
                "Home Team": home_team,
                "Away Team": away_team,
                "Highest Home Odds": highest_odds["Home"],
                "Highest Draw Odds": highest_odds["Draw"],
                "Highest Away Odds": highest_odds["Away"],
                "Source Home": sources["Home"],
                "Source Draw": sources["Draw"],
                "Source Away": sources["Away"]
            })
        else:

            output_data.append({

                "Home Team": home_team,
                "Away Team": away_team,
                "Highest Home Odds": highest_odds["Highest Home Odds"],
                "Highest Draw Odds": highest_odds["Highest Draw Odds"],
                "Highest Away Odds": highest_odds["Highest Away Odds"],
                "Source Home": sources["Highest Home Odds"],
                "Source Draw": sources["Highest Draw Odds"],
                "Source Away": sources["Highest Away Odds"]
            })
        for non_matching_matches in non_corresponding_matches:
            try:
                if (i == 0):
                    output_data.append({
                    "Home Team": non_matching_matches["Home Team"],
                    "Away Team": non_corresponding_matches["Away Team"],
                    "Highest Home Odds": non_corresponding_matches["Home"],
                    "Highest Draw Odds": non_corresponding_matches["Draw"],
                    "Highest Away Odds": non_corresponding_matches["Away"],
                    "Source Home": source_name1,
                    "Source Draw": source_name1,
                    "Source Away": source_name1
                    })
                else:
                    output_data.append({
                    "Home Team": non_matching_matches["Home Team"],
                    "Away Team": non_corresponding_matches["Away Team"],
                    "Highest Home Odds": non_corresponding_matches["Highest Home Odds"],
                    "Highest Draw Odds": non_corresponding_matches["Highest Draw Odds"],
                    "Highest Away Odds": non_corresponding_matches["Highest Away Odds"],
                    "Source Home": non_matching_matches["Source Home"],
                    "Source Draw": non_matching_matches["Source Draw"],
                    "Source Away": non_matching_matches["Source Away"]
                    })
            except:
                pass

unique_output_data = [dict(t) for t in {tuple(d.items()) for d in output_data}]
# Save output data as JSON in the Betdata folder
output_folder = "Intermediatevalues"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save output data as JSON in the Intermediatevalues folder
output_file_path = os.path.join(output_folder, "games.json")
with open(output_file_path, "w") as outfile:
    json.dump(unique_output_data, outfile, indent=4)

print(f"Output saved as 'games.json' in the {output_folder} folder.")
