# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Initialize the browser.
# Create a data dictionary.
# End the WebDriver and return the scraped data.


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "mars_hemispheres": hemispheres(browser)

    }


    # Stop webdriver and return data
    browser.quit()
    return data


# Scrape Mars News
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page, 1 second
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    
    return news_title, news_p


def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button (the 2nd button in inspect 9 buttons)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url



def mars_facts():

    # Add try/except for error handling
    try:
        
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")



def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
   
    for x in range(4):
        hemispheres = {}
        browser.links.find_by_partial_text('Hemisphere')[x].click()
        
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        
        title = hemi_soup.find('h2', class_='title').text
        hemi_url=browser.find_by_text('Sample')['href']
    
        hemispheres['img_url'] = hemi_url
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        
        browser.back()

    return hemisphere_image_urls



if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

