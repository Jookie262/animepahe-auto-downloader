from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Put anime text here
anime = "Futoku no Guild"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://animepahe.com/")
time.sleep(2)

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
