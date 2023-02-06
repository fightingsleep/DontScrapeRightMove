import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd

PATH_TO_CHROME_DRIVER = "C:\\Users\\chris\\Downloads\\chromedriver_win32"

# This is just an example. Don't actually scrape rightmove, it's not allowed.
WEBSITE_URL = "https://www.rightmove.co.uk/"

# TODO: Make these params
LOCATION_TO_SEARCH = "SE10"
SORT_ORDER = "Newest Listed"

def main() -> None:
    os.environ["PATH"] += os.pathsep + PATH_TO_CHROME_DRIVER

    # Start the web driver and load the website
    driver = webdriver.Chrome()
    driver.get(WEBSITE_URL)
    driver.implicitly_wait(0.5)

    # Locate the search box and the 'For Sale' button on the home page
    search_box = driver.find_element(by=By.NAME, value="typeAheadInputField")
    for_sale_button = driver.find_element(by=By.XPATH, value="//button[text()='For Sale']")

    # Enter the location and proceed to the next page
    search_box.send_keys(LOCATION_TO_SEARCH)
    for_sale_button.click()

    # Click 'Find properties' button to perform the search
    find_properties_button = driver.find_element(by=By.XPATH, value="//button[text()='Find properties']")
    find_properties_button.click()

    # Choose the sort order
    select_element = driver.find_element(By.ID, 'sortType')
    select = Select(select_element)
    select.select_by_visible_text(SORT_ORDER)

if __name__ == "__main__":
    main()