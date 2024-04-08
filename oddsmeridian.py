import re
from bs4 import BeautifulSoup
import json
import os
# Sample HTML content
with open('meridianbet', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all match info containers
match_infos = soup.find_all('standard-item-info', class_='event ng-star-inserted')

# Abbreviations to remove
# Create an empty list to store match data
match_data = []

# Function to remove abbreviations from team names
def remove_abbreviations(team_name):
    return re.sub(r'\b[A-Z]+\b', '', team_name)

# Process each match
for match_info in match_infos:
    # Extract team names (same logic as before)
    rivals = match_info.find('div', class_='rivals')
    if rivals:
        home_team = rivals.find('div', class_='home').text.strip()
        away_team = rivals.find('div', class_='away').text.strip()

        # Remove abbreviations
        home_team = remove_abbreviations(home_team)
        away_team = remove_abbreviations(away_team)

        # Find the odds container (same logic as before)
        odds_container = match_info.find('standard-item-games', class_='games g3 ng-star-inserted')

        # Extract and store odds
        if odds_container:
            odds_elements = odds_container.find_all('div', class_='odds ng-star-inserted')
            if len(odds_elements) >= 3:  # Check if there are at least 3 odds elements
                home_win_odds = odds_elements[0].text.strip()
                draw_odds = odds_elements[1].text.strip()
                away_win_odds = odds_elements[2].text.strip()

                # Create a dictionary for this match data
                match_dict = {
                    "Home Team": home_team,
                    "Away Team": away_team,
                    "Home": home_win_odds,
                    "Draw": draw_odds,
                    "Away": away_win_odds,
                }
                match_data.append(match_dict)

# Save match data as JSON
folder_name = "Betdata"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the file path including the folder name
file_path = os.path.join(folder_name, "meridianbet.json")

# Write the JSON data to the file inside the folder
with open(file_path, 'w') as json_file:
    json.dump(match_data, json_file, indent=4)