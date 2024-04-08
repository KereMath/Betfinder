import requests
import json

# URL to scrape
url = "https://meridianbet.me/sails/sport-with-leagues/58/date/2024-04-03T20:24:36+03:00/filter/oneDay/filterPosition/0,0,0"

# Make a GET request to fetch the raw HTML content
response = requests.get(url)
if response.status_code == 200:
    # Assuming the response content is JSON
    data = response.json()
    
    # Save the JSON data to a file
    with open('meridianbetdata.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print("Data saved to soccerbetdata.json")
else:
    print("Failed to retrieve data. Status code:", response.status_code)