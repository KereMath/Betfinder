from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


# Assuming you've already initialized your WebDriver instance
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the webpage
driver.get("https://www.premier-kladionica.com/ponuda/")

# Find the element you want to hover over
option1_XPATH_BASE = "/html/body/div[1]/div/div[3]/div[1]/div/div/div/ul/li["


for i in range(1,30):
    option1_XPATH = option1_XPATH_BASE + str(i) + "]"
    option1 = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, option1_XPATH))
    )
    if (option1.text[0] == 'S' and option1.text[1] == 'V' and option1.text[2] == 'E'):
        break

option2_XPATH_BASE = option1_XPATH + "/div/ul/li["

action = ActionChains(driver)
action.move_to_element(option1).perform()
time.sleep(1)
for i in range(1, 30):
    option2_XPATH = option2_XPATH_BASE + str(i) + "]"
    option2 = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, option2_XPATH))
    )
    if (option2.text[0:7] == "NOGOMET"):
        break
option2.click()

time.sleep(25)
match_info_list = []
for j in range(2, 120):
    for i in range(1, 200):
        match_XPATH = "/html/body/div[1]/div/div[3]/div[3]/div/div/div[2]/div["+str(j)+"]/div/table/tbody/tr["+str(i)+"]"
        try:
            # Find the element with a timeout of 0.1 seconds
            match = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, match_XPATH)))
            tr_element_html = match.get_attribute('outerHTML')

            # Parse the HTML
            soup = BeautifulSoup(tr_element_html, 'html.parser')

            # Extract team names
            td_element = soup.find('td', class_='cmd')


            # Remove all <span> elements inside <td> element
            for span in td_element.find_all('span'):
                span.decompose()

            # Get the text content after removing <span> elements
            stripped_text = td_element.get_text(strip=True)

            try:
                team1, team2 = stripped_text.split('-')
            except:
                continue
            # Extract odds for winning, drawing, and losing
            odds = {}
            odds_elements = soup.find_all('td', class_='cmd')[1:4]
            for index, element in enumerate(odds_elements, start=1):
                key = 'Winning' if index == 1 else ('Drawing' if index == 2 else 'Losing')
                odds[key] = element.text.strip()
            odds = {key: value.replace(',', '.') for key, value in zip(['Winning', 'Drawing', 'Losing'], [element.text.strip() for element in odds_elements])}
            # Print the results
            match_info_dict = {
            "Home Team": team1.strip(),
            "Away Team": team2.strip(),
            "Home": float(odds['Winning']),
            "Draw": float(odds['Drawing']),
            "Away": float(odds['Losing'])
            }
            match_info_list.append(match_info_dict)
        except TimeoutException:
            break
       
file_path = "Betdata/Kladionica.json"    

# Write the list of dictionaries to a JSON file
with open(file_path, "w") as json_file:
    json.dump(match_info_list, json_file, indent=4)




driver.quit()
print("Klaudionica data has been scraped and saved to kladionica.json.")