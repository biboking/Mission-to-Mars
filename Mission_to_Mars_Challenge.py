#!/usr/bin/env python
# coding: utf-8

# In[25]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[26]:


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[27]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page, 1 second
browser.is_element_present_by_css('div.list_text', wait_time=1)


# 1. we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as \<ul class="item_list"\>.
# 
# 2. we're also telling our browser to wait one second before searching for components.

# In[28]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent (the other tags within the \<div \/\> element)? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a \<li \/\> element with a class of slide and all nested elements within it.

# In[29]:


# assign the title and summary text to variables we'll reference later.
slide_elem.find('div', class_='content_title')


# we chained .find onto our previously assigned variable, slide_elem. When we do this, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data."

# In[30]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[31]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[32]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[33]:


# Find and click the full image button (the 2nd button in inspect 9 buttons)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[34]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[35]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[36]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[37]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[38]:


df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# - df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# - df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
# - df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.

# In[39]:


# add the dataframe back as table to my own webpage
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles 

# ## 1. Using Browser for the full-image link
# 
# ##### - No need to add the orriginal URL

# ### Hemispheres

# In[153]:


# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)


# In[170]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# html = browser.html
# mysoup = soup(html, 'html.parser')
# mysoup


# In[171]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    
for x in range(4):
    hemispheres = {}
    browser.links.find_by_partial_text('Hemisphere')[x].click()
    
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    title = hemi_soup.find('h2', class_='title').text
    hemi_url=browser.find_by_text('Sample')['href']
   
    
    print(title)
    print(hemi_url)
    hemispheres['img_url'] = hemi_url
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()
   


# In[172]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[152]:


# 5. Quit the browser
browser.quit()


# ## 2. Using Beautifulsoup for the full-image link
# 
# ##### - Need to add the original/home /index URL

# In[173]:


url = 'https://marshemispheres.com/'
browser.visit(url)


# In[174]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    
for x in range(4):
    hemispheres = {}
    browser.links.find_by_partial_text('Hemisphere')[x].click()
    
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    
    title = hemi_soup.find('h2', class_='title').text
    hemi_url= hemi_soup.find('li').a['href']
    #hemi_url= hemi_soup.find('li').a.get('href')
    img_url=f'https://marshemispheres.com/{hemi_url}'
    
    print(title)
    print(hemi_url)
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[175]:


hemisphere_image_urls


# In[176]:


browser.quit()


# In[ ]:




