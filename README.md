# 🚫Dont Scrape RightMove🚫

Scraping [rightmove.co.uk](https://www.rightmove.co.uk/) would be against their terms of service, so don't do it.

This repo contains an example of how you can use [Selenium](https://www.selenium.dev/) as a web scraper to hypothetically scrape listing data from RightMove. There is absolutely more efficient ways to do this, but I wanted to learn about Selenium.

It currently scrapes for listings with two bathrooms. This is useful because RightMove doesn't allow you to filter on the number of bathrooms for some reason.

This can easily be modified to scrape for other types of listings, just edit the `scrape_page_of_listings` function to whatever suits your needs 