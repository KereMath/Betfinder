from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json

start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
# Set up Selenium webdriver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sbbet.me/sport?event_type=upcoming")
driver.maximize_window()

# Specify the XPath of the parent div that contains the data you want to scrape
scrollable_XPATH = "/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div/div/div"


# Wait for the parent div to be present in the DOM
target_element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, scrollable_XPATH))
)

match_info_array = []
for j in range(30):
    for i in range(1, 24):

        match_XPATH = "/html/body/div[1]/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div/div/div/div[1]/div[1]/div[" + str(i) + "]"

        try:
            
            # Try to locate the match element
            
            match = WebDriverWait(driver, 0.01).until(
                EC.presence_of_element_located((By.XPATH, match_XPATH))
            )
            match_info = match.text.split("\n")
            match_info_array.append([match_info[3], match_info[4], match_info[5], match_info[6], match_info[7]])

        except:
            #If element not found, perform scrolling action here
            pass


    target_element.send_keys(Keys.PAGE_DOWN)
            

        
match_info_set = set(map(tuple, match_info_array))

match_info_list = []
for match_info_tuple in match_info_set:
    if (match_info_tuple[2] == "-" or match_info_tuple[3] == "-" or match_info_tuple[4] == "-"):
        continue
    match_info_dict = {
        "Home Team": match_info_tuple[0],
        "Away Team": match_info_tuple[1],
        "Home": float(match_info_tuple[2]),
        "Draw": float(match_info_tuple[3]),
        "Away": float(match_info_tuple[4])
    }
    match_info_list.append(match_info_dict)

# Define the file path
file_path = "Betdata/Sbbet.json"

# Write the list of dictionaries to a JSON file
with open(file_path, "w") as json_file:
    json.dump(match_info_list, json_file, indent=4)


driver.quit()
print("Execution time: " + str(time.time() - start_time) + " seconds.")
print("SBbet data has been scraped and saved to Sbbet.json.")
