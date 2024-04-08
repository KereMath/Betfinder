import json
import requests


# URL to scrape
url = "https://www.soccerbet.me/restapi/offer/sr_ME/sport/S/mob?annex=0&desktopVersion=2.27.46&locale=sr_ME"

# Make a GET request to fetch the raw HTML content
response = requests.get(url)
if response.status_code == 200:
    # Assuming the response content is JSON
    data = response.json()
    
    # Save the JSON data to a file
    with open('soccerbetdata.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
else:
    print("Failed to retrieve data. Status code:", response.status_code)
# Load the JSON data from 'soccerbetdata.json'
with open('soccerbetdata.json', 'r') as infile:
    data = json.load(infile)

# Initialize an empty list to hold the simplified matches data
simplified_matches = []

# Check if 'esMatches' is in the data and process each match
if 'esMatches' in data:
    for match in data['esMatches']:
        # Extract the odds for "Home win", "Draw", "Away win" assuming the keys are consistent
        # Note: This assumes that the odds are available and correctly indexed. You may need to add checks or try-except blocks.
        home_odds = str(match.get("betMap", {}).get("1", {}).get("NULL", {}).get("ov", "N/A"))
        draw_odds = str(match.get("betMap", {}).get("2", {}).get("NULL", {}).get("ov", "N/A"))
        away_odds = str(match.get("betMap", {}).get("3", {}).get("NULL", {}).get("ov", "N/A"))

        match_data = {
            "Home Team": match.get("home", "N/A"),
            "Away Team": match.get("away", "N/A"),
            "Home": float(home_odds),
            "Draw": float(draw_odds),
            "Away": float(away_odds)
        }
        simplified_matches.append(match_data)

# Save the simplified matches data to 'soccerbet.json'
with open('Betdata/soccerbet.json', 'w') as outfile:
    json.dump(simplified_matches, outfile, ensure_ascii=False, indent=4)

print("Processed data saved to soccerbet.json")
