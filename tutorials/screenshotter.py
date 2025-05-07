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

if __name__ == "__main__":
    if len(sys.argv) < 2: # Ensures all required arguments are given
        print("Usage: python main.py <url> [--screenshot]")
        sys.exit(1)
        
    url = sys.argv[1]
    take_screenshot = '--screenshot' in sys.argv

    with sync_playwright() as playwright:
        run(playwright, url, take_screenshot)