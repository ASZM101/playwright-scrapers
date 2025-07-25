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
    # Still need to add specific details to collect, maybe defaults for now, user-specified later

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
    logger.info(f"Login successful") # Still need to remove this, just testing

# Define CLI to use click for scraping process
@click.command()
@click.option("--config", type=click.Path(exists=True), default="my_config.yaml", help="Path to the YAML config file") # Still need to change default to colleges_config.yaml
@click.option("--headless/--no-headless", default=False, help="Run the browser in headless mode or not") # Still need to change default to False

def main(config, headless):
    with open(config, "r") as f: # Load YAML file with list of search params
        data = yaml.safe_load(f)
    
    email = data.get("email")
    password = data.get("password")
    # Still need to add params

    with sync_playwright() as p: # Start browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        login(page, email, password, headless) # Log in to Going Merry
        browser.close()

if __name__ == '__main__':
    main()