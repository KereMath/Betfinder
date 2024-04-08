import os
import re
import json
from bs4 import BeautifulSoup

# Read the contents of the file
with open("combined_content.html", "r") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# List of abbreviations to remove
abbreviation_removals = {
    'FC': None,
    'SC': None,
    'AC': None,
    'AFC': None,
    'CFC': None,
    'MU': None,
    'AS': None,
    'BK': None,
    'CA': None,
    'CF': None,
    'KS': None,
    'PFC': None,
    'PV': None,
    'SK': None,
    'SP': None,
    'SS': None,
    'WFC': None,
    'CP': None
}

# Function to remove abbreviations from team names
def remove_abbreviations(team_name):
    for abbreviation in abbreviation_removals.keys():
        team_name = re.sub(r'\b' + abbreviation + r'\b', '', team_name)
    return team_name.strip()

# Find all tr elements with class 'matches'
matches = soup.find_all('tr', class_='matches')

# Extract team names and odds for each match
matches_info = []
for match in matches:
    team_names = [a.text.strip() for a in match.find_all('a', class_='match_item')]
    # Remove abbreviations
    team_names = [remove_abbreviations(name) for name in team_names]
    odds_spans = match.find_all('span')
    odds = [span.text.strip() for span in odds_spans]
    match_info = {"Home Team": team_names[0], "Away Team": team_names[1], "Home": odds[2], "Draw": odds[3], "Away": odds[4]}
    matches_info.append(match_info)

# Create a folder named "Betdata"
folder_name = "Betdata"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the file path including the folder name
file_path = os.path.join(folder_name, "hatbet.json")

# Save match data as JSON inside the folder
with open(file_path, 'w') as json_file:
    json.dump(matches_info, json_file, indent=4)
