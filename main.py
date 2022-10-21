from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://animepahe.com/")
time.sleep(2)

# Search anime 
search = driver.find_element("name", "q")
search.send_keys("Boruto");
time.sleep(2)


