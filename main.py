from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# Open Animepahe Website
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://animepahe.com/")
time.sleep(2)

# Put anime text here
anime = "Spy X Family"

# Search anime 
search = driver.find_element("name", "q")
search.send_keys(anime + " ");
time.sleep(2)

# Click the first element in the result 
try:
    search_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    )
    first_element = search_result.find_element(By.TAG_NAME, "li").find_element(By.TAG_NAME, "a")
    first_element.send_keys(Keys.ENTER);
    time.sleep(2)
except:
    print("Anime Not Found!");

# Get the total number of Anime Episodes
total_episode = driver.find_element(By.CLASS_NAME, "episode-count")
num_episode = re.findall(r'[0-9]+', total_episode.text)
print(num_episode[0])

# Click Ascending Button
ascending_btn = driver.find_element(By.ID, "episode_asc")
ascending_btn.send_keys(Keys.ENTER)