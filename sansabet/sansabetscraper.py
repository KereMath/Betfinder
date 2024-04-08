import json
import requests
# The endpoint URL
url = "https://sansabet.com/Oblozuvanje.aspx/GetLiga"
ligaID = []
for i in range(1, 5000):
    ligaID.append(i)
# The JSON body you want to send
data = {
    "LigaID": ligaID,
    "filter": "0",
    "parId": 0
}

# The headers to be sent with the request
headers = {'Content-Type': 'application/json'}

# Sending the POST request
response = requests.post(url, json=data, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    # Saving the response content to a file
    with open('response_data.json', 'w',encoding="utf-8") as file:
        json.dump(response.json(), file, indent=4)
    
else:
    print(f"Failed to send request. Status code: {response.status_code}")

# Load the JSON data from the file
input_file_path = 'response_data.json'  # Make sure this path is correct
with open(input_file_path, 'r') as file:
    long_json = json.load(file)

games_data = []
for data_structure in long_json:

    if "P" in data_structure:
        for game in data_structure["P"]:
            teams = game["PN"].split(" : ")
            home_team = teams[0]
            away_team = teams[1]

            odds_dict = {"Home": None, "Draw": None, "Away": None}

            for odd in game["T"][:3]:
                if odd["TP"] == "1":
                    val1=odds_dict["Home"] = odd["K"]
                elif odd["TP"] == "X":
                    val2=odds_dict["Draw"] = odd["K"]
                elif odd["TP"] == "2":
                    val3=odds_dict["Away"] = odd["K"]
            flag=0
            if(isinstance(val1,float) and isinstance(val2,float) and isinstance(val3,float)):
                flag=1
            if (isinstance(val1,float) and isinstance(val2,float) and isinstance(val3,float)):
                if val1<5.0 and val2>10.0 and val3<5.0:
                    flag=0
            
            if(flag==1):
                games_data.append({
                    "Home Team": home_team,
                    "Away Team": away_team,
                    "Home": odds_dict["Home"],
                    "Draw": odds_dict["Draw"],
                    "Away": odds_dict["Away"]
                })

# Save the games_data list to a JSON file
output_file_path = 'Betdata/SansaBet.json'  # Adjust this path if needed
with open(output_file_path, 'w') as file:
    json.dump(games_data, file, indent=4)

print("Data saved to sansabet.json successfully.")
