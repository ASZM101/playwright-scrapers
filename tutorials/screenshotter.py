import sys # Import modules
import re
from playwright.sync_api import sync_playwright

def run(playwright, url, take_screenshot):
    browser = playwright.chromium.launch() # Launch Chromium headless browser
    page = browser.new_page()
    page.goto(url) # Proceed to requested page

    if take_screenshot: # Save page screenshot as PNG if requested
        __capture_screenshot(page)
    else:
        __save_page_text(page, "body")
    
    browser.close() # Close browser

def __save_page_text(page, selector):
    title = page.title() # Get page title
    content = page.query_selector(selector) # Get requested element
    text = (content.inner_text() if content else "No requested selector found") # Extract element text content

    filename = __safe_filename_from(title) # Use regex to create safe filename from title by removing any invalid chars and replacing space with underscores

    with open(filename, "w", encoding="utf-8") as f: # Write page title and main text to file named after page title
        f.write(f"Title: {title}\n\n")
        f.write(text)
    
    print(f"Data saved as {filename}")

def __safe_filename_from(title):
    safe_title = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_") # Removes any chars that are not word chars, spaces, or dashes; removes leading/trailing whitespace characters; replaces spaces with underscores
    return f"{safe_title}.txt"

def __capture_screenshot(page):
    page.screenshot(path="screenshot.png", full_page=True) # full_page set to True to take care of long pages with scrolling
    print("Screenshot saved as screenshot.png")

if __name__ == "__main__":
    if len(sys.argv) < 2: # Ensures all required arguments are given
        print("Usage: python main.py <url> [--screenshot]")
        sys.exit(1)
        
    url = sys.argv[1]
    take_screenshot = '--screenshot' in sys.argv

    with sync_playwright() as playwright:
        run(playwright, url, take_screenshot)