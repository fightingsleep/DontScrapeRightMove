import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

PATH_TO_CHROME_DRIVER = "C:\\Users\\chris\\Downloads\\chromedriver_win32"

# This is just an example. Don't actually scrape rightmove, it's not allowed.
WEBSITE_URL = "https://www.rightmove.co.uk/"

def main() -> None:
    os.environ["PATH"] += os.pathsep + PATH_TO_CHROME_DRIVER

    # Start the web driver and load the website
    driver = webdriver.Chrome()
    driver.get(WEBSITE_URL)
    driver.implicitly_wait(0.5)

    # Locate the search box and the for sale button
    search_box = driver.find_element(by=By.NAME, value="typeAheadInputField")
    for_sale_button = driver.find_element(by=By.XPATH, value="//button[text()='For Sale']")

if __name__ == "__main__":
    main()