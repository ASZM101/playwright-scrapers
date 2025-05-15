# Finds scholarships on scholarship site using provided credentials and parameters/filters; WIP

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

# dataclass (decorator from dataclasses module, automatically generates special methods) stores info about each scholarship listing
@dataclass
class Scholarship:
    url: str
    title: str
    org: str
    amount: str
    recipients: str
    deadline: str

def login(page, email, password, headless): # Log in to scholarship site using provided credentials (need to set up config.yaml first)
    page.goto("https://app.goingmerry.com/sign-in") # Go to scholarship site login page
    page.wait_for_load_state("load")

    # Fill in login credentials
    page.get_by_placeholder("Email").click()
    page.get_by_placeholder("Email").fill(email)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(password)

    page.get_by_text("Sign in").click() # Click login btn
    page.wait_for_load_state("load")

    if "checkpoint/challenge" in page.url and not headless: # Detects if CAPTCHA page encountered
        logger.warning("CAPTCHA page: Human interventions is required")
        while True: # Polling loop to check if CAPTCHA is solved
            if "checkpoint/challenge" not in page.url:
                logger.info("CAPTCHA solved. Continuing with the rest of the process...")
                break
            page.wait_for_timeout(2000) # Wait 2 sec before polling again
        page.wait_for_timeout(5000) # Wait 5 sec after CAPTCHA solved
    else:
        logger.error("CAPTCHA page: Aborting due to headless mode...")
        sys.exit(1)

def scrape_scholarships(page, params): # Scrape scholarship listings based on provided search parameters (include in config.yaml)
    base_url = "https://app.goingmerry.com/awards"
    url = f"{base_url}?eg=mat,par&{urlencode(params)}"

    scholarship_list = [] # List for storing scholarship data

    page.goto(url) # Go to search results page
    page.wait_for_load_state("load")

    cards = page.locator("div.widget-award-wrapper")
    for i in range(cards.count()): # Loop through scholarship listings
        card = cards.nth(i)
        card.click()
        page.wait_for_timeout(3000) # Wait 3 sec while scholarship card loads
        info = Scholarship(
            url=card.locator("a.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.gm-button.variant-secondary.size-medium.margins.bottom-10.MuiButton-disableElevation.MuiButton-fullWidth").get_attribute("href"),
            title=card.locator("#award-name").text_content(),
            org=card.locator("h5.neutral-color.margins top-2").text_content(),
            amount=card.locator("div.award-quick-action-box.card.white.z-depth-1").locator("h2").text_content(),
            recipients=card.locator("div.award-quick-action-box.card.white.z-depth-1").locator("b").text_content(),
            deadline=card.locator("div.award-quick-action-box.card.white.z-depth-1").locator("p.blue-grey-text").text_content()
        ) # Scrapes details of each scholarship
        scholarship_list.append(info)
        logger.info(f"Scraped scholarship: {info.title}")
        if i >= 5: # Stops scraping once 5 scholarships found (can be changed, good starting point)
            break
    
    return scholarship_list

# Define CLI to use click for scraping process
@click.command()
@click.option("--config", type=click.Path(exists=True), default="config.yaml", help="Path to the YAML config file")
@click.option("--headless/--no-headless", default=True, help="Run the browser in headless mode or not")

def main(config, headless):
    with open("config.yaml", "r") as f: # Load YAML file with list of search params
        data = yaml.safe_load(f)

    email = data.get("email")
    password = data.get("password")
    params_list = data.get("params")
    
    with sync_playwright() as p: # Start browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        login(page, email, password, headless) # Log in to scholarship site

        all_scholarships = []
        for params in params_list:
            logger.info(f"Crawl starting... Params: {params}")
            scholarships = scrape_scholarships(page, params)
            all_scholarships.extend(scholarships)
        
        df = pd.DataFrame([scholarship.__dict__ for scholarship in all_scholarships]) # Create DataFrame from combined scholarships

        csv_file_path = 'scholarships_data.csv'
        df.to_csv(csv_file_path, index=False) # Save DataFrame to CSV file

        logger.info(f"Scraped {len(all_scholarships)} scholarships and saved to scholarships_data.csv") # Log the number of scholarships scraped and saved

        browser.close()

if __name__ == '__main__':
    main()