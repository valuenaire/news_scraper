# News Scraper Project

## Description

This News Scraper is a Python-based tool designed to extract news articles from various online sources. It automates the process of collecting news data, providing users with up-to-date information on various topics.

## Features

- Scrapes news from multiple sources.
- Batch processing capabilities for efficiency.
- Summarization feature using a pre-trained NLP model.
- Customizable scraping settings (e.g., frequency, sources).

## Requirements

- Python 3.x
- Libraries: requests, BeautifulSoup, pandas, transformers, torch, tqdm.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/valuenaire/news_scraper.git
   pip3 install requests beautifulsoup4 pandas transformers torch tqdm
   ```

## Output

- it will give csv file so with following columns

| title | link | time | text | summary |
| ----- | ---- | ---- | ---- | ------- |
