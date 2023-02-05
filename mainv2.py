# Animepahe Auto Downloader
# Automated Anime Downloading from the Animepahe Website Using Selenium Python
# Created by: Jookie262

# Import Libraries
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

# Ask User Input for the Anime Name and the quality of the video
anime = input("Enter the name of the anime: ")
pixels = input("Enter the quality of the video (720 or 1080): ")

# Set up Chrome Driver and the options needed
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("start-maximized") 
options.add_extension('fdm.crx')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
actionChains = ActionChains(driver)

# Open Animepahe Website
driver.get("https://animepahe.com/")
time.sleep(2)

# Type the anime text in the search bar
try:
    search = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search.send_keys(anime + " ")
except:
    print("Error in searching anime")
    driver.quit()

# Click the first element in the result
try:
    search_result = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    )
    first_element = search_result.find_element(By.TAG_NAME, "li").find_element(By.TAG_NAME, "a")
    first_element.send_keys(Keys.ENTER)
except:
    print("Anime Not Found!")
    driver.quit()

# Click Ascending Button
try:
    ascending_btn = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "episode_asc"))
    )
    actionChains.double_click(ascending_btn).perform()
except:
    print("Error in clicking Ascending Button")
    driver.quit()

# Get the total number of Anime Episodes
try:
    total_episode = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "episode-count"))
    )
    num_episode = re.findall(r'[0-9]+', total_episode.text)
except:
    print("Error in getting the total number of episodes")
    driver.quit()

# Click the first episode
try:
    time.sleep(1)
    first_episode = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "episode-list"))
    )
    first_episode_div = first_episode.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a")
    first_episode_div.send_keys(Keys.ENTER);
    time.sleep(2)
except:
    print("Error in clicking the first episode")
    driver.quit()

# Loop through all the episodes from 1 to the total number of episodes
for i in range(int(num_episode[0])):

    # Click the download button
    try:
        download_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "downloadMenu"))
        )
        download_btn.send_keys(Keys.ENTER)
        time.sleep(2)
    except:
        print("Error in clicking the download button")
        driver.quit()

    # Click the pixels you want
    try:
        dropdown_download = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "pickDownload"))
        )
        driver.implicitly_wait(5)
        choices = dropdown_download.find_elements(By.CLASS_NAME, "dropdown-item")

        for choice in choices:      
            if pixels + "p" in choice.text:
                choice.send_keys(Keys.ENTER)
    except:
        print("Error in clicking the pixels you want")
        driver.quit()

    # Click Pahewin Continue button
    driver.switch_to.window(driver.window_handles[-1])
    while True:
        try:
            countinue_vid = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Continue"))
            )
            if countinue_vid:
                countinue_vid.send_keys(Keys.ENTER)
                break
            else:
                driver.refresh()
        except:
            print("Error in clicking continue button");

    # Click Download button in Kwik
    while True:
        try:
            kwik_download_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )

            if kwik_download_btn:
                # kwik_download_btn.send_keys(Keys.ENTER)
                print(f"Downloading Episode {i + 1}")
                break
            else:
                driver.refresh()

        except:
            print("Error in clicking download button in Kwik")
            driver.quit()
    
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
        driver.quit()