import requests
import os
import json
url = "https://sportdataprovider-volcano.xtreme.bet/api/public/prematch/SportEvents?SportId=1&timezone=-180&t=b7a855b8-4f88-4d95-8f7b-c4527826bb08&clientType=WebConsumer&v=1.1.1417&lang=sr-Latn-ME"

payload = {}
headers = {
  'authority': 'sportdataprovider-volcano.xtreme.bet',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
  'if-modified-since': 'Tue, 02 Apr 2024 15:46:41 GMT',
  'origin': 'https://www.volcanobet.me',
  'referer': 'https://www.volcanobet.me/',
  'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
}

response = requests.request("GET", url, headers=headers, data=payload)

json_data = json.loads(response.text)
sum=0
match_data=[]
for location in json_data["locations"]:    
    for league in location["leagues"]:        
        for eventDateGroup in league["eventDateGroups"]:            
            for event in eventDateGroup["events"]:
                data={}
                data["Home Team"]=event["fixture"]["participants"][0]["name"]
                data["Away Team"]=event["fixture"]["participants"][1]["name"]
                for market in event["markets"]:
                    if market["marketId"]=="1":
                        data["Home"]=market["picks"][0]["odds"]
                        data["Draw"]=market["picks"][1]["odds"]
                        data["Away"]=market["picks"][2]["odds"]
                        
                match_data.append(data)
                

import os
folder_name = "Betdata"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the file path including the folder name
file_path = os.path.join(folder_name, "volcano.json")

# Write the JSON data to the file inside the folder
with open(file_path, 'w',encoding="utf8") as json_file:
    json.dump(match_data, json_file, indent=4)
