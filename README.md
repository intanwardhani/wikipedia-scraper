![](https://img.shields.io/badge/Python-14354C?style=flat&logo=python&logoColor=white) ![](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white) ![](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

# About Me
New to the field of data science, this was my first data scraping attempt. I realised that scraping information from an API endpoint was quite doable, as compared to wild webscraping. (I like to call webscraping 'wild webscraping', using wildberries hunting as analogy.)

My least favourite thing in this project is regular expression (regex). Regex cheatsheets will always be useful to have!

# Overview
This wikipedia-scraper uses the `country-leaders.onrender.com` API to retrieve a list of countries, fetch leaders for each country, and obtain the raw Wikipedia pages for each leader. The scraped results are still raw, therefore a sanitising is necessary to make it legible. The sanitising using regular expression (regex) is used. This method is expected to work across different languages. However, the current results are still not perfect and each language may need different regex sanitisation.

This project is part of Data Science & AI Bootcamp by BeCode in winter 2025/2026.

# Project Structure
```markdown
wikipedia-scraper
├── LICENSE
├── README.md
├── leaders.json                (Final results in .json format)
├── leaders_workflow.log        (Workflow logbook)
├── main.py                     (Main script to run the scraper)
├── paragraphs.csv              (Final results in .csv format)
├── wikipedia_scraper.ipynb     (Workflow notebook)
└── wikiscrapers
    ├── filemanager.py          (Export-import class)
    ├── leaders.py              (Fetch data from API)
    └── paragraphs.py           (Paragraphs sanitiser using regex)
```
