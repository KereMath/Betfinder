import os
import requests
import json
leagues = ['173411', '102168', '160560', '145394', '102152', '102153', '102155', '102157', '158859', '102203', '102598', '102527', '159081', '102758', '102999', '174791', '164084', '164083', '144511', '133619', '160267', '125895', '102139', '148868', '161041', '128892', '159396', '130270', '130271', '159389', '102896', '102357', '102240', '154610', '164873', '164874', '177094', '161232', '162162', '174085', '161583', '130930', '130856', '164389', '164432', '102597', '159879', '102143', '102728', '102208', '159651', '132262', '159393', '160394', '158854', '159185', '175601', '175600', '158857', '160489', '159999', '135084', '135083', '140760', '130263', '162262', '131059', '114950', '102615', '102165', '102150', '102151', '125660', '136245', '141565', '121123', '102320', '102321', '102154', '102246', '102205', '102169', '102258', '160490', '158769', '102599', '130269', '130438', '125693', '159678', '159657', '134663', '135463', '156641', '102247', '132701', '132700', '158824', '160242', '160243', '112627', '102846', '112202', '158723', '128157', '135384', '159364', '159186', '159676', '129008', '102335', '159783', '159614', '102189', '160102', '160806', '163383', '163382', '158856', '158761', '102816', '144428', '130642', '130607', '130555', '135122', '102206', '102248', '158772', '160887', '102738', '102170', '102191', '102209', '102210', '131938', '160861', '130646', '130647', '160103', '161274', '102192', '160360', '131911', '102922', '102346', '102347', '102160', '102251', '127248', '134644', '134645', '131978', '131979', '131977', '132077', '102161', '102434', '128015', '102348', '170521', '158758', '160080', '102211', '150569', '162380', '161445']

def getLeague(league):
    url = f"https://www.lobbet.me/ibet/offer/league/{league}/-1/0/false.json?v=4.58.21&locale=en&ttgIds="
    payload = {}
    headers = {
    'authority': 'www.lobbet.me',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'SESSION=e8e8ba06-51a8-42f0-9063-09cd6a288eaf; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=en',
    'referer': 'https://www.lobbet.me/ibet-web-client/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data=json.loads(response.text)
    matches=json_data["matchList"]
    if matches==None:
        return

    
    for match in matches:
        data={}
        try:
            data["Home Team"]=match["home"]
            data["Away Team"]=match["away"]
            data["Home"]=match["odBetPickGroups"][0]["tipTypes"][0]["value"]
            data["Draw"]=match["odBetPickGroups"][0]["tipTypes"][1]["value"]
            data["Away"]=match["odBetPickGroups"][0]["tipTypes"][2]["value"]
            match_data.append(data)
        except:
            pass

        

match_data=[]

for league in leagues:
    getLeague(league)

folder_name = "Betdata"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Specify the file path including the folder name
file_path = os.path.join(folder_name, "lobbet.json")

# Write the JSON data to the file inside the folder
with open(file_path, 'w') as json_file:
    json.dump(match_data, json_file, indent=4)
print("Lobbet data has been scraped and saved to lobbet.json.")