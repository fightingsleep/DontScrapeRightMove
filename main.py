import os
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# This is just an example. Don't actually scrape rightmove, it's not allowed.
WEBSITE_URL = "https://www.rightmove.co.uk/"

PATH_TO_CHROME_DRIVER = "C:\\Users\\chris\\Downloads\\chromedriver_win32"

DEFAULT_LOCATION_TO_SEARCH = "London"
DEFAULT_SORT_ORDER = "Newest Listed"
DEFAULT_ADDED_TO_SITE = "Last 24 hours"

def scrape_page_of_listings(driver: webdriver) -> list[str]:
    """This function scrapes a page of listings and extracts links to all listings with 2 bathrooms

    Args:
        driver (webdriver): The Selenium web driver

    Returns:
        list[str]: A list of links to 2 bathroom listings
    """
    links_we_care_about = []

    # Loop through the listings
    listings = driver.find_elements(by=By.CLASS_NAME, value="l-searchResult")
    for listing in listings:
        # Lets only consider the listings with 2 bathrooms and ignore the featured listings
        try:
            is_featured = listing.find_elements(by=By.CLASS_NAME, value="propertyCard--featured")
            if len(is_featured) != 0:
                continue

            bathroom_element = listing.find_element(by=By.XPATH, value=".//span[@class='no-svg-bathroom-icon bathroom-icon seperator']/*[local-name()='svg' and namespace-uri()='http://www.w3.org/2000/svg']/*[local-name()='title']")
            num_bathrooms = bathroom_element.get_attribute("textContent")
            if num_bathrooms == "2 bathrooms":
                links_we_care_about.append(listing.find_element(by=By.XPATH, value=".//a[@class='propertyCard-link property-card-updates']").get_attribute("href"))
        except:
            continue

    return links_we_care_about

def main() -> None:
    os.environ["PATH"] += os.pathsep + PATH_TO_CHROME_DRIVER

    parser = argparse.ArgumentParser(
        prog="DontScrapeRightMove",
        description="Scrapes listing data from rightmove.co.uk")
    parser.add_argument("-l", "--location", help="The location to search for listings")
    parser.add_argument("-s", "--sortorder", help="The order in which to sort the listings " +
        "valid values are: 'Newest Listed', 'Oldest Listed', 'Highest Price', 'Lowest Price'")
    parser.add_argument("-a", "--addedtosite", help="The time span over which to search for listings " +
        "valid values are: 'Anytime', 'Last 24 hours', 'Last 3 days', 'Last 7 days', 'Last 14 days'")
    args = parser.parse_args()

    location_to_search = DEFAULT_LOCATION_TO_SEARCH
    if args.location is not None:
        location_to_search = args.location

    sort_order = DEFAULT_SORT_ORDER
    if args.sortorder is not None:
        sort_order = args.sortorder

    added_to_site = DEFAULT_ADDED_TO_SITE
    if args.addedtosite is not None:
        added_to_site = args.addedtosite

    # Start the web driver and load the website
    driver = webdriver.Chrome()
    driver.get(WEBSITE_URL)
    driver.implicitly_wait(0.5)

    # Locate the search box and the 'For Sale' button on the home page
    search_box = driver.find_element(by=By.NAME, value="typeAheadInputField")
    for_sale_button = driver.find_element(by=By.XPATH, value="//button[text()='For Sale']")

    # Enter the location and proceed to the next page
    search_box.send_keys(location_to_search)
    for_sale_button.click()

    # Click 'Find properties' button to perform the search
    find_properties_button = driver.find_element(by=By.XPATH, value="//button[text()='Find properties']")
    find_properties_button.click()

    # Choose the sort order
    sort_order_select_element = driver.find_element(By.ID, "sortType")
    sort_order_select = Select(sort_order_select_element)
    sort_order_select.select_by_visible_text(sort_order)

    # Open the filters section
    filter_button = driver.find_element(by=By.CLASS_NAME, value="filtersBar-more")
    filter_button.click()

    # Choose the time span
    time_span_select_element = driver.find_element(By.NAME, "addedToSite")
    time_span_select = Select(time_span_select_element)
    time_span_select.select_by_visible_text(added_to_site)

    # Click the 'Accept Cookies' button that seems to always pop up here
    accept_cookies_button = driver.find_element(by=By.CLASS_NAME, value="accept-cookies-button")
    accept_cookies_button.click()

    # TODO: There appears to be an issue with the chrome driver that makes it struggle to click buttons
    # that are wrapped in empty <div></div>. This is a workaround to be able to close the filters window
    filter_button.send_keys('\n')

    links_we_care_about = []
    there_is_another_page = True
    while there_is_another_page:
        # Scrape the current page of listings
        links_we_care_about.extend(scrape_page_of_listings(driver))

        # Try clicking on the next page button
        try:
            next_button = driver.find_element(By.XPATH, "//button[@class='pagination-button pagination-direction pagination-direction--next']")
            there_is_another_page = next_button.is_enabled()
            if there_is_another_page:
                next_button.click()
            else:
                there_is_another_page = False
        except:
            there_is_another_page = False

    print('\n\n\n' + '\n'.join(map(str, links_we_care_about)) + '\n\n\n')

if __name__ == "__main__":
    main()
