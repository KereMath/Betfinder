import requests
import json
import os
from fake_useragent import UserAgent

# Instantiate the UserAgent class
ua = UserAgent()
url = "https://api.maxbet.me/bonus?lang=en&limit=9999&markets=ofb,ofbs,of0s,obb,obbs,otn,ovb,ohb,oih,oaf,ott,oft,osn,osns,orb,obs,obx,obxs,odt,owp,obm,ocr,omm,oe0s,os2s,op1s,oj0s,obf,&offset=0"
# Get random user agents
random_ua = ua.random

# Randomize all headers
headers = {
  'authority': ua.random,
  'accept': ua.random,
  'accept-language': ua.random,
  'origin': ua.random,
  'referer': ua.random,
  'sec-ch-ua': ua.random,
  'sec-ch-ua-mobile': ua.random,
  'sec-ch-ua-platform': ua.random,
  'sec-fetch-dest': ua.random,
  'sec-fetch-mode': ua.random,
  'sec-fetch-site': ua.random,
  'user-agent': random_ua
}



payload = {}

response = requests.request("GET", url, headers=headers, data=payload)
print(response)
json_data = json.loads(response.text)
matches = json_data["events"]
match_data = []
for match in matches:
    if match["id"].split(":")[1] != "fb":
        break
    data = {}
    data["Home Team"] = match["competitors"][0]["name"]
    data["Away Team"] = match["competitors"][1]["name"]
    data["Home"] = match["odds"]["ofb:fs:1"]["value"]
    data["Draw"] = match["odds"]["ofb:fs:X"]["value"]
    data["Away"] = match["odds"]["ofb:fs:2"]["value"]
    match_data.append(data)

folder_name = "Betdata"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the file path including the folder name
file_path = os.path.join(folder_name, "maxbet.json")

# Write the JSON data to the file inside the folder
with open(file_path, 'w') as json_file:
    json.dump(match_data, json_file, indent=4)
