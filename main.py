import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

PATH_TO_CHROME_DRIVER = "C:\\Users\\chris\\Downloads\\chromedriver_win32"

# This is just an example. Don't actually scrape rightmove, it's not allowed.
WEBSITE_URL = "https://www.rightmove.co.uk/"

# TODO: Make these params
LOCATION_TO_SEARCH = "SE10"
SORT_ORDER = "Newest Listed"
ADDED_TO_SITE = "Last 24 hours"

def main() -> None:
    os.environ["PATH"] += os.pathsep + PATH_TO_CHROME_DRIVER

    # Start the web driver and load the website
    driver = webdriver.Chrome()
    driver.get(WEBSITE_URL)
    driver.implicitly_wait(5)

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
    sort_order_select_element = driver.find_element(By.ID, "sortType")
    sort_order_select = Select(sort_order_select_element)
    sort_order_select.select_by_visible_text(SORT_ORDER)

    # Open the filters section
    filter_button = driver.find_element(by=By.CLASS_NAME, value="filtersBar-more")
    filter_button.click()

    # Choose the time span
    time_span_select_element = driver.find_element(By.NAME, "addedToSite")
    time_span_select = Select(time_span_select_element)
    time_span_select.select_by_visible_text(ADDED_TO_SITE)

    # Click the 'Accept Cookies' button that seems to always pop up here
    accept_cookies_button = driver.find_element(by=By.CLASS_NAME, value="accept-cookies-button")
    accept_cookies_button.click()

    # TODO: There appears to be an issue with the chrome driver that makes it struggle to click buttons
    # that are wrapped in empty <div></div>. This is a workaround to be able to close the filters window
    filter_button.send_keys('\n')

    # Loop through the listings
    listings = driver.find_elements(by=By.XPATH, value="//div[@id='l-searchResults']/div/div")
    listing_we_care_about = []
    for listing in listings:
        is_featured = listing.find_elements(by=By.CLASS_NAME, value="propertyCard--featured")
        if len(is_featured) != 0:
            continue
        # Lets only consider the listings with 2 bathrooms
        num_bathrooms = listing.find_element(by=By.XPATH, value=".//span[@class='no-svg-bathroom-icon']/svg/title").text
        if num_bathrooms == "2 bathrooms":
            listing_we_care_about.add(listing)

    input("Press enter to exit")

if __name__ == "__main__":
    main()