from contextlib import nullcontext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import time

# Open Animepahe Website
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("start-maximized") 
options.add_extension('fdm.crx')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://animepahe.com/")
actionChains = ActionChains(driver)
time.sleep(2)

# Put anime text here
anime = "Mairimashita! Iruma-kun 3rd Season"

# Type the quality of video here  
pixels = "720"

# Search anime 
search = driver.find_element("name", "q")
search.send_keys(anime + " ")
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
try:
    ascending_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "episode_asc"))
    )
    actionChains.double_click(ascending_btn).perform()
except:
    print("Error in clicking Ascending Button");

time.sleep(5)

# Click First Episode
try:
    first_episode = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "episode-list"))
    )
    first_episode_div = first_episode.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a")
    first_episode_div.send_keys(Keys.ENTER);
    time.sleep(2)
except:
    print("First Episode Not Found");


# Loop through all episodes
for i in range(int(num_episode[0])):
    
    time.sleep(3)

    # Click the download button
    try:
        download_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "downloadMenu"))
        )
        download_btn.send_keys(Keys.ENTER)
    except:
        print("Error in clicking download button");

    # Click 720p Link
    try:
        dropdown_download = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pickDownload"))
        )
        driver.implicitly_wait(5)
        choices = dropdown_download.find_elements(By.CLASS_NAME, "dropdown-item")

        for choice in choices:      
            if pixels + "p" in choice.text:
                choice.send_keys(Keys.ENTER)
        
    except:
        print("Error in clicking 720 link");

    # Click Pahewin Continue button
    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(5)

    try:
        countinue_vid = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Continue"))
        )
        countinue_vid.send_keys(Keys.ENTER)
    except:
        print("Error in clicking continue button");

    # Click Download button in Kwik
    kwik_download_btn = driver.find_element(By.TAG_NAME, "button")
    kwik_download_btn.send_keys(Keys.ENTER)
    time.sleep(5)

    # Close the kwik tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(2)

    # Click the next episode button
    try:
        next_episode = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[title^='Play Next Episode']"))
        )
        next_episode.send_keys(Keys.ENTER)
    except:
        print("Error in clicking next episode button");
