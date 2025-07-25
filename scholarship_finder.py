# Finds scholarships on Going Merry (scholarship and college database) using provided credentials and parameters/filters

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

def login(page, email, password, headless): # Log in to Going Merry using provided credentials (need to create account and set up scholarships_config.yaml first)
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

def scrape_scholarships(max, page, params): # Scrape scholarship listings based on provided search parameters (include in scholarships_config.yaml)
    base_url = "https://app.goingmerry.com/awards"
    url = f"{base_url}?{urlencode(params)}"

    scholarship_list = [] # List for storing scholarship data

    page.goto(url) # Go to search results page
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000) # Wait 3 sec to ensure page loads

    cards = page.locator("div.widget-award-wrapper")
    for i in range(cards.count()): # Loop through scholarship listings
        card = cards.nth(i)
        card.click()
        page.wait_for_timeout(2000) # Wait 2 sec while scholarship preview loads
        preview = page.locator("div.MuiPaper-root.MuiDialog-paper.widget-award-preview-dialog__paper.MuiDialog-paperScrollPaper.MuiDialog-paperWidthMd.MuiPaper-elevation24.MuiPaper-rounded")
        response = Selector(text=preview.inner_html())
        info = Scholarship(
            url=response.css("a.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.gm-button.variant-secondary.size-medium.margins.bottom-10.MuiButton-disableElevation.MuiButton-fullWidth ::attr(href)").get() if response.css("a.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.gm-button.variant-secondary.size-medium.margins.bottom-10.MuiButton-disableElevation.MuiButton-fullWidth ::attr(href)").get() else None,
            
            title=response.css("#award-name ::text").get() if response.css("#award-name ::text").get() else None,
            
            org=response.css("h5.neutral-color.margins.top-2 ::text").get() if response.css("h5.neutral-color.margins.top-2 ::text").get() else None,
            
            amount=response.css("div.award-quick-action-box.card.white.z-depth-1 h2 ::text").get() if response.css("div.award-quick-action-box.card.white.z-depth-1 h2 ::text").get() else None,
            
            recipients=response.css("div.award-quick-action-box.card.white.z-depth-1 b ::text").get() if response.css("div.award-quick-action-box.card.white.z-depth-1 b ::text").get() else None,
            
            deadline=response.css("div.award-quick-action-box.card.white.z-depth-1 p.blue-grey-text ::text").get() if response.css("div.award-quick-action-box.card.white.z-depth-1 p.blue-grey-text ::text").get() else None
        ) # Scrapes details of each scholarship
        scholarship_list.append(info)
        logger.info(f"Scraped scholarship: {info.title}")
        page.get_by_text("Close", exact=True).click() # Click close btn
        page.wait_for_timeout(1000) # Wait for 1 sec to account for lagginess in closing card
        if i == max - 1: # Stops scraping once max scholarships found
            break
    
    return scholarship_list

# Define CLI to use click for scraping process
@click.command()
@click.option("--max", default=5, help="Specify a maximum number of scholarships to scrape")
@click.option("--config", type=click.Path(exists=True), default="scholarships_config.yaml", help="Path to the YAML config file")
@click.option("--headless/--no-headless", default=True, help="Run the browser in headless mode or not")

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

        all_scholarships = []
        for params in params_list:
            logger.info(f"Initiating search... Params: {params}")
            scholarships = scrape_scholarships(max, page, params)
            all_scholarships.extend(scholarships)
        
        df = pd.DataFrame([scholarship.__dict__ for scholarship in all_scholarships]) # Create DataFrame from combined scholarships

        csv_file_path = 'scholarships_data.csv'
        df.to_csv(csv_file_path, index=False) # Save DataFrame to CSV file

        logger.info(f"Scraped {len(all_scholarships)} scholarships and saved to scholarships_data.csv") # Log the number of scholarships scraped and saved

        browser.close()

if __name__ == '__main__':
    main()