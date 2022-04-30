from selenium import webdriver as wd
import requests
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time

# For each book
# Retrieve information from Amazon,Barnes and Noble, Powells(price, reviews, availability, etc.)
# Compute the most favorable one using a custom metric
# Order the book online using selenium


options = wd.ChromeOptions()
options.add_argument('--headless')

# Getting data from Amazon
wd = wd.Chrome()

wd.implicitly_wait(10)
wd.get("https://www.amazon.com/")
search_bar = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input")
time.sleep(5)
search_bar.send_keys("978-0262046305")
time.sleep(5)
search_button = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
search_button.click()
time.sleep(15)

product_name = []
product_asin = []
product_price = []
product_ratings = []
product_ratings_num = []
#product_link = []

items_all = wait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
items_sponsored = wait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "AdHolder")]')))
items = [item for item in items_all if item not in items_sponsored]
for item in items:
    # find name
    name = item.find_element(by=By.XPATH, value='.//span[@class="a-size-medium a-color-base a-text-normal"]')
    product_name.append(name.text)

    # find ASIN number
    data_asin = item.get_attribute("data-asin")
    product_asin.append(data_asin)

    # find price
    whole_price = item.find_elements(by=By.XPATH, value='.//span[@class="a-price-whole"]')
    fraction_price = item.find_elements(by=By.XPATH, value='.//span[@class="a-price-fraction"]')

    if whole_price != [] and fraction_price != []:
        price = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        price = 0
    product_price.append(price)

    # find ratings box
    ratings_box = item.find_elements(by=By.XPATH, value='.//div[@class="a-row a-size-small"]/span')

    # find ratings and ratings_num
    if ratings_box != []:
        ratings = ratings_box[0].get_attribute('aria-label')
        ratings_num = ratings_box[1].get_attribute('aria-label')
    else:
        ratings, ratings_num = 0, 0

    product_ratings.append(ratings)
    product_ratings_num.append(str(ratings_num))

    # find link
    #link = item.find_element(by=By.XPATH, value='.//a[@class="a-link-normal a-text-normal"]').get_attribute("href")
    #product_link.append(link)

wd.quit()

# to check data scraped
print(product_name)
print(product_asin)
print(product_price)
print(product_ratings)
print(product_ratings_num)
#print(product_link)