# Planning

## Web Scraper Ideas
- 🚧 College searcher (in progress)
- Job finder (WIP, fix bugs)
- Screenshotter (WIP, add more unique features)
- Sitemap scanner (WIP, add more unique features)
- ✅ Scholarship finder (MVP done)

### College Searcher
- Based on scholarship finder
    - Collect info from each university
    - Add info to CSV
    - Have failsafe in case university name mistyped or not available on platform
- Potential college database platforms (ensure any user can create free account)
    - Going Merry (uses URL params)
    - Niche
    - College Vine
    - CollegeXpress
    - Appily
- Create new YAML files (private and template)
    - Info for user to input
        - List of universities (full name)
        - Specific details to collect about each university
    - Updates to scholarship finder YAML
        - Rename YAML files for scholarship finder
        - Update YAML file names in readme for scholarship finder
- Update readme with info about college searcher
    - Overall description
    - Technical requirements
    - How to run
    - Options for details to collect
    - Table of contents
- Create "experienceable build"
    - Record video of college searcher in action
    - Take screenshot of college searcher alone
    - Take screenshot of both scholarship finder and college searcher together (main screenshot)
- Restructure folders
    - Make each scraper have its own folder with Python, YAML, screenshot, and recording files
    - Update all file paths in Python files and readme instructions
- Add comments to explain what each imported library/module is for in each file
- Test both scrapers as external user (starting with downloading repo from GitHub)