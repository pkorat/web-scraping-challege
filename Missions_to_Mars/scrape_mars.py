# Parth Korat
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():

    # init return dictionary
    scraped_data = {}

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    scraped_data['News Title'] = news_title
    scraped_data['News Paragraph'] = news_p

    # second page
    url_2 = 'https://spaceimages-mars.com/'
    browser.visit(url_2)

    html_2 = browser.html
    soup_2 = bs(html_2, 'html.parser')

    featured_image_url = soup_2.find('img', {'class': "headerimage fade-in"})['src']

    scraped_data['Image URL'] = featured_image_url

    # third page
    url_3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url_3)

    mars_facts_df = pd.concat([tables[0].drop(2, axis=1), tables[1]]).drop(0, axis=0).reset_index()

    mars_facts_df_clean = mars_facts_df.drop('index', axis=1)

    mars_facts_df_clean.columns = ['Properties', 'Mars']

    html_mars_ftable = mars_facts_df_clean.to_html().replace('\n', '')

    scraped_data['Mars Facts'] = html_mars_ftable

    # forth page
    url_4 = 'https://marshemispheres.com/'
    browser.visit(url_4)

    html_3 = browser.html
    soup_3 = bs(html_3, 'html.parser')

    hrefs = soup_3.findAll('h3')
    hemisphere_image_urls = []

    for i in range(len(hrefs)-1):
        browser.links.find_by_partial_text(hrefs[i].text).click()
        html_i = browser.html
        soup_i = bs(html_i, 'html.parser')
        
        hemisphere_image_urls.append({'title': hrefs[i].text, 
                                    'img_url': browser.links.find_by_partial_text('Sample')[0]['href']})
        browser.visit(url_4)
    
    scraped_data['Hemisphere Images'] = hemisphere_image_urls

    return scraped_data