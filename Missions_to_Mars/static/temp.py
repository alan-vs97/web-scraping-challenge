# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Open browser
executable_path = {'executable_path': 'c:/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# Get data from news site

url_news = 'https://mars.nasa.gov/news/'
browser.visit(url_news)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# Find the first article
news = soup.find('div', class_='list_text')

# Find the title and the parragraph
title_news = news.a.text
p_news = news.find('div', class_='article_teaser_body').text

print(title_news)
print(p_news)
