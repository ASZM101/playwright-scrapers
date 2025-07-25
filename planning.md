# Planning

## Web Scraper Ideas
- 🚧 College searcher (in progress)
- ⏸️ Job finder (on pause, fix bugs)
- ⏸️ Screenshotter (on pause, add more unique features)
- ⏸️ Sitemap scanner (on pause, add more unique features)
- ✅ Scholarship finder (MVP done)

## General Updates
- Take screenshot of outputs of all scrapers together (main screenshot)
- Allow user to specify what details they want to collect with each scraper (explain options available in readme)
- Restructure folders
    - Make each scraper have its own folder with Python, YAML, screenshot, and recording files
    - Update all file paths in Python files and readme instructions
- Update readme with options for all possible URL params for each scraper
- Add comments to explain what each imported library/module is for in each Python file
- Enable scraping programs to search in multiple pages
- Test all scrapers as external user (starting with downloading repo from GitHub)
- ✅ Add table of contents

## College Searcher
- ✅ Based on scholarship finder
    - ✅ **Explore**: Find information on colleges that meet criteria provided by user (more similar to scholarships, **_start here_**)
        - ✅ Apply parameters provided by user
        - ✅ Collect info from each college
        - ✅ Add info to CSV
    - **Find**: Find information on specific colleges based on full name provided by user (more similar to using platform to search for college on platform, but easier to mass-collect info using terminal, **_later_**)
        - Input full name of college into search bar
        - Collect info from each college
        - Add info to CSV
        - Have failsafe in case college name mistyped or not available on platform
    - Mode specified as flag (WIP)
        - Option 1: True/false flag where one mode is true and other is false
        - Option 2: 2 flags, one for each mode
- ✅ Create new YAML template file
    - ✅ Login credentials (both modes, required)
    - Specific details to collect about each college (both modes, optional)
    - ✅ URL parameters (only explore, required)
    - Full names of colleges (only find, required)
    - Specific details to collect about each college
- ✅ Update readme with info about college searcher (need to update once both modes finished)
    - ✅ Overall description
    - ✅ Technical requirements
    - ✅ How to run
- Create "experienceable build"
    - Record video of college searcher in action
    - Take screenshot of college searcher alone

## Scholarship Finder
- ✅ Update readme with info about scholarship finder
    - ✅ Overall description
    - ✅ Technical requirements
    - ✅ How to run
- ✅ Based on job finder tutorial
    - ✅ Apply parameters provided by user
    - ✅ Collect info from each scholarship
    - ✅ Add info to CSV
- ✅ Create YAML template file (seaparate from personal file)
    - ✅ Login credentials (required)
    - ✅ URL parameters (eg=mat and hide=COS as default)
- ✅ Create "experienceable build"
    - ✅ Record video of scholarship finder in action
    - ✅ Take screenshot of college searcher alone
- ✅ Rename YAML file names and update readme