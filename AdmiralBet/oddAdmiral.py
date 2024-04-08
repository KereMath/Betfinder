import json
import os
import requests
match_data=[]
def scraper(page):
    url = "https://webapi.admiralbet.me/SportBookCacheWeb/api/offer/getEventsStartingSoonFilterSelections/"
    params = {
        'sportId': '1',
        'topN': '25',
        'skipN': str((page-1)*25),
        'isLive': 'false',
        'dateFrom': '2024-04-02T11:28:49.715',
        'dateTo': '2029-04-02T11:28:19.000',
        'eventMappingTypes': '',
        'pageId': '3'
    }

    headers = {
        'Accept': 'application/utf8+json, application/json, text/plain, */*',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Language': 'sr-Latn',
        'OfficeId': '1175',
        'Origin': 'https://www.admiralbet.me',
        'Referer': 'https://www.admiralbet.me/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    try:
        response = requests.get(url, params=params, headers=headers)

    except requests.exceptions.RequestException as e:
        raise e("VPN is not connected or check your internet connection")
        
    try:
        matches=json.loads(response.text)
    except:
        raise("Error in parsing response, please check the response")
    if(len(matches)==0):
        return -1
    dictList=[]
    for match in matches:
        data={}
        try:
            data["Home Team"]=match["name"].split("-")[0].strip()
            data["Away Team"]=match["name"].split("-")[1].strip()        
            data["Home"]=match ["bets"][0]["betOutcomes"][0]["odd"]
            data["Draw"]=match ["bets"][0]["betOutcomes"][1]["odd"]
            data["Away"]=match ["bets"][0]["betOutcomes"][2]["odd"]
            dictList.append(data)
            pass
        except:
            pass
    
    return dictList


def scrapeThemAll():
    page=1
    while(1):
        data=scraper(page)
        if(data==-1):
            break
        else:            
            match_data.extend(data) 
            page+=1
        
    
    
scrapeThemAll()
    


# Specify the file path including the folder name
file_path = "Betdata/admiral.json"

# Write the JSON data to the file inside the folder
with open(file_path, 'w') as json_file:
    json.dump(match_data, json_file, indent=4)
print("Admiral data has been scraped and saved to admiral.json.")