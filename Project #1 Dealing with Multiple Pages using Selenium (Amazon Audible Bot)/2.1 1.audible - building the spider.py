from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# define the website to scrape and path where the chromediver is located
website = 'https://www.audible.com/search'
# define 'driver' variable
driver = webdriver.Chrome()
# open Google Chrome with chromedriver
driver.get(website)
driver.maximize_window() #instead of it being cropped like a mini window

containers=driver.find_elements(By.CLASS_NAME,'adbl-impression-container')

# Getting all the audiobooks listed (the "/" gives immediate child nodes)
for container in containers:
    products = container.find_elements(By.XPATH,'.//li[contains(@class, "productListItem")]')
# products = container.find_elements_by_xpath('./li')

# Initializing storage
book_title = []
book_author = []
book_length = []
# Looping through the products list (each "product" is an audiobook)
for product in products:
    # We use "contains" to search for web elements that contain a particular text, so we avoid building long XPATH
    book_title.append(product.find_element(By.XPATH,'.//h3[contains(@class, "bc-heading")]').text)  # Storing data in list
    book_author.append(product.find_element(By.XPATH,'.//li[contains(@class, "authorLabel")]').text)
    book_length.append(product.find_element(By.XPATH,'.//li[contains(@class, "runtimeLabel")]').text)

driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)