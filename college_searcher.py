# Collects information from colleges on Going Merry (scholarship and college database) using provided credentials and parameters/filters

import yaml
from urllib.parse import urlencode, urljoin
from playwright.sync_api import sync_playwright
from scrapy import Selector
from dataclasses import dataclass
import pandas as pd
import logging
import re
from rich.logging import RichHandler
import click
import sys

# logging module is for better log outputs; rich library enhances logging with additional formatting (ex. colors)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
rich_handler = RichHandler(rich_tracebacks=True)
logging.getLogger().handlers = [rich_handler]

# dataclass (decorator from dataclasses module, automatically generates special methods) stores info about each college
@dataclass
class College:
    url: str
    name: str
    location: str
    rates: str
    cost: str

def login(page, email, password, headless): # Log in to Going Merry using provided credentials (need to create account and set up colleges_config.yaml first)
    page.goto("https://app.goingmerry.com/sign-in") # Go to Going Merry login page
    page.wait_for_load_state("load")

    # Fill in login credentials
    page.get_by_placeholder("Email").click()
    page.get_by_placeholder("Email").fill(email)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(password)

    page.get_by_text("Sign in", exact=True).click() # Click login btn
    page.wait_for_timeout(3000) # Wait 3 sec to ensure page loads
    page.wait_for_load_state("load")

def explore_colleges(max, page, params): # Scrape info about colleges based on provided search parameters (include in colleges_config.yaml)
    base_url = "https://app.goingmerry.com/colleges"
    url = f"{base_url}?{urlencode(params)}"

    college_list = [] # List for storing college info

    page.goto(url) # Go to search results page
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000) # Wait 3 sec to ensure page loads

    # Still need to iterate through results max times (WIP)
    cards = page.locator("div.college-list")
    for i in range(cards.count()): # Loop through colleges
        card = cards.nth(i)
        selector = Selector(text=card.inner_html())
        info = College(
            url = base_url + selector.css("a.college-name ::attr(href)").get() if selector.css("a.college-name ::attr(href)").get() else None,

            name = selector.css("a.college-name ::text").get() if selector.css("a.college-name ::text").get() else None,

            location = selector.css("div.location-year-wrapper span ::text").get() if selector.css("div.location-year-wrapper span ::text").get() else None,

            rates = selector.css("p.rates ::text").get() if selector.css("p.rates ::text").get() else None,

            cost = selector.css("span.cost-text").get() + "/yr" if selector.css("span.cost-text").get() else None
        ) # Scrapes details of each college
        college_list.append(info)
        logger.info(f"Scraped college: {info.name}")
        if i == max - 1: # Stops scraping once max scholarships found
            break

    return college_list

# Define CLI to use click for scraping process
@click.command()
@click.option("--max", default=5, help="Specify a maximum number of colleges to scrape")
@click.option("--config", type=click.Path(exists=True), default="my_config.yaml", help="Path to the YAML config file") # Still need to change default to colleges_config.yaml (at end)
@click.option("--headless/--no-headless", default=False, help="Run the browser in headless mode or not") # Still need to change default to False (at end)

def main(max, config, headless):
    with open(config, "r") as f: # Load YAML file with list of search params
        data = yaml.safe_load(f)
    
    email = data.get("email")
    password = data.get("password")
    params_list = data.get("params")

    with sync_playwright() as p: # Start browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        login(page, email, password, headless) # Log in to Going Merry

        all_colleges = []
        for params in params_list:
            logger.info(f"Initiating search... Params: {params}")
            colleges = explore_colleges(max, page, params)
            all_colleges.extend(colleges)

        df = pd.DataFrame([college.__dict__ for college in all_colleges]) # Create DataFrame from combined colleges

        csv_file_path = 'colleges_data.csv'
        df.to_csv(csv_file_path, index=False) # Save DataFrame to CSV file

        logger.info(f"Scraped {len(all_colleges)} colleges and saved to colleges_data.csv")

        browser.close()

if __name__ == '__main__':
    main()