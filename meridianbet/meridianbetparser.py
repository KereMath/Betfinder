import json

def process_meridianbet_data(filename):
    # Read the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Initialize an empty list to store the formatted match data
    formatted_data = []
    
    # Assuming your JSON structure contains multiple match entries
    for match in data.get("team", []):
        # Extract home and away team names
        home_team = match["team"][0]["name"]
        away_team = match["team"][1]["name"]
        
        # Assuming the odds are stored in a similar way for each match
        odds = match["standardShortMarkets"][0]["selection"]
        home_odds = odds[0]["price"]
        draw_odds = odds[1]["price"]
        away_odds = odds[2]["price"]
        
        # Append the formatted match data to the list
        formatted_data.append({
            "Home Team": home_team,
            "Away Team": away_team,
            "Home": home_odds,
            "Draw": draw_odds,
            "Away": away_odds
        })
    
    # Optionally, save the formatted data back to a new JSON file or print it
    with open('formatted_meridianbet_data.json', 'w') as outfile:
        json.dump(formatted_data, outfile, indent=4)
    
    # Print formatted data to console (optional)
    print(json.dumps(formatted_data, indent=4))

# Replace 'meridianbetdata.json' with the actual path to your JSON file
process_meridianbet_data('meridianbetdata.json')
