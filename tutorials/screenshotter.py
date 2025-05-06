import sys # Import modules
from playwright.sync_api import sync_playwright

def run(playwright, url, take_screenshot):
    browser = playwright.chromium.launch() # Launch Chromium headless browser
    page = browser.new_page()
    page.goto(url) # Proceed to requested page

    if take_screenshot: # Save page screenshot as PNG if requested
        page.screenshot(path="screenshot.png", full_page=True) # full_page set to True to take care of long pages with scrolling
        print("Screenshot saved as screenshot.png")
    
    browser.close() # Close browser