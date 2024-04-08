from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# Initialize WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
# Set up Selenium webdriver
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

# Open the webpage
driver.get("https://www.hatbet.me/Home/Sportsbook/Fudbal")

data = []  # Initialize an empty list to store data

try:
    for i in range(1,2):  # Assuming there are up to 10 categories, adjust as necessary
        # Click on the first level item
        first_level_xpath = f'//*[@id="Sports"]/ul/li[{i}]/a'
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, first_level_xpath))).click()

        for j in range(1, 84):  # Assuming each category could have up to 10 subcategories, adjust as necessary
            # Attempt to click on the second level item
            second_level_xpath = f'//*[@id="Sports"]/ul/li[{i}]/div/ul/li[{j}]/a'
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, second_level_xpath))).click()
            except TimeoutException:
                break  # Exit the loop if no more subcategories are found

            k = 1
            while True:  # Loop indefinitely until a condition breaks it
                third_level_xpath = f'//*[@id="Sports"]/ul/li[{i}]/div/ul/li[{j}]/div/ul/li[{k}]'
                try:
                    # Attempt to click on the third level item
                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, third_level_xpath))).click()
                    # If successful, add page source or specific data to your data list

                    # You may need to navigate back or refresh depending on the website's behavior
                    # driver.back()
                    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, first_level_xpath))).click()
                    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, second_level_xpath))).click()

                    k += 1  # Move to the next item
                except TimeoutException:
                    break  # Exit the loop if no more items are found
        soup = BeautifulSoup(driver.page_source, 'html.parser')        
        relevant_elements = soup.find_all('td', class_=lambda x: x and ('match_odds_visibility' in x.split() or 'bet-odd' in x.split() or 'match_odd bet-odd first-column-of-market' in x.split()))
        data = '\n'.join([str(elem) for elem in relevant_elements])
        
finally:
    driver.quit()

    # Save the extracted page source to an HTML file
    with open('hatbet.html', 'w', encoding='utf-8') as f:
        # Assuming `data` contains HTML content. If `data` is a list, you might join it or iterate to write.
        for page_html in data:
            f.write(page_html)
    
    
# Function to parse the HTML and extract details for all games
def parse_all_game_details(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize a list to store details of all games
    all_game_details = []

    # Find all match details
    match_details_containers = soup.find_all('td', class_='match_odds_visibility')
    
    for match_details in match_details_containers:
        teams = match_details.get_text().split(' - ')
        if len(teams) == 2:
            home_team, away_team = teams[0].strip(), teams[1].strip()

            # Initialize the odds list
            odds = []

            # First, get the odds from the first-column-of-market
            first_odd_element = match_details.find_next_sibling('td', class_='match_odd bet-odd first-column-of-market')
            if first_odd_element and first_odd_element.find('span'):
                odds.append(first_odd_element.find('span').get_text())

            # Then, get the next two odds from match_odd bet-odd
            next_odd_elements = first_odd_element.find_next_siblings('td', class_='match_odd bet-odd', limit=2) if first_odd_element else []
            for odd_element in next_odd_elements:
                if odd_element and odd_element.find('span'):
                    odds.append(odd_element.find('span').get_text())

            # Make sure we have exactly 3 odds, else fill missing with "N/A"
            odds += ["N/A"] * (3 - len(odds))

            # Construct the game details dictionary
            game_details = {
                "Home Team": home_team,
                "Away Team": away_team,
                "Home": float(odds[0]),
                "Draw": float(odds[1]),
                "Away": float(odds[2])
            }

            # Append the game details to the list of all games
            all_game_details.append(game_details)

    return all_game_details

# Parse the game details from 'hatbet.html'
all_game_details = parse_all_game_details("hatbet.html")

# Save the extracted details to 'allgames.json'
with open('Betdata/hatbet.json', 'w', encoding='utf-8') as f:
    json.dump(all_game_details, f, indent=4)

print("Details of all games have been saved to hatbet.json.")
