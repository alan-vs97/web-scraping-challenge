# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# This function returns all the scraped data and updates table.html
def scrape():

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

    # Get image URL
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url_image)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the button that leads to the full image
    news = soup.find('a', class_='button fancybox')

    # Go to article with full image
    browser.visit(f"https://www.jpl.nasa.gov/{news['data-link']}")

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find list of download links
    images = soup.find_all('div', class_='download_tiff')

    # Find jpg format link. Exit loop as soon as there is a match
    for image in images:
        if "jpg" in image.a['href']:
            featured_image_url = "http:" + image.a['href']
            break
    
    # Get tweets URL
    url_weather = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url_weather)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the first tweet in the timeline
    tweet = soup.find('div', class_="js-tweet-text-container")

    # Get only the thext of the tweet, substracting the url of the image that came with the tweet
    weather_text = tweet.p.text.replace(tweet.p.a.text, "")

    #Get facts URL
    url_facts = 'https://space-facts.com/mars/'

    browser.visit(url_facts)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the table
    table = soup.find('table', class_="tablepress tablepress-id-p-mars")

    # Pass table to pandas
    pd_table = pd.read_html(str(table))[0]

    # Save table as html
    table_html = pd_table.to_html(header=False, index=False)
    # Get hemispheres URL
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_hemispheres)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find all hemispheres
    results = soup.find_all('div', class_="description")

    hemisphere_image_urls = []

    for result in results:
        browser.visit('https://astrogeology.usgs.gov' + result.a['href'])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find('div', class_="downloads").find('a')

        image_dict = {
            "title": result.a.text,
            "link": links['href']
        }

        hemisphere_image_urls.append(image_dict)

    # We return everything but the table facts since that one is saved directly as an html file
    return title_news, p_news, featured_image_url, weather_text, hemisphere_image_urls, table_html
