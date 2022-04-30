from selenium import webdriver as wd
import requests
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time

options = wd.ChromeOptions()
options.add_argument('--headless')

# Getting data from Amazon
wd = wd.Chrome()

wd.implicitly_wait(10)
wd.get("https://www.barnesandnoble.com/")
search_bar = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/nav/div/div[3]/form/div/div[2]/div/input[1]")
time.sleep(5)
search_bar.send_keys("978-0262046305")
time.sleep(5)
search_button = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/nav/div/div[3]/form/div/span/button")
search_button.click()
time.sleep(15)

product_name = []
#product_asin = []
product_price = []
#product_ratings = []
#product_ratings_num = []
#product_link = []


#items = wait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "product-shelf-tile-book")]')))
#for item in items:
    # find name
    #link_name = item.find_element(by=By.TAG_NAME, value='a')
    #name = link_name.get_attribute("title")
    #product_name.append(name)

    # find ASIN number
    #data_asin = item.get_attribute("data-asin")
    #product_asin.append(data_asin)

    # find price
    #price = item.find_element(by=By.TAG_NAME, value='a')
    #price_text = item.find_element(by=By.XPATH, value='.//div[contains(@class, "product-shelf-pricing")]').text
    #price = (price_text.split('$'))[1]
    #product_price.append(price)



    # find ratings box
    #ratings_box = item.find_elements(by=By.XPATH, value='.//div[@class="a-row a-size-small"]/span')

    # find ratings and ratings_num
    #if ratings_box != []:
        #ratings = ratings_box[0].get_attribute('aria-label')
        #ratings_num = ratings_box[1].get_attribute('aria-label')
    #else:
        #ratings, ratings_num = 0, 0

    #product_ratings.append(ratings)
    #product_ratings_num.append(str(ratings_num))

    # find link
    #link = item.find_element(by=By.XPATH, value='.//a[@class="a-link-normal a-text-normal"]').get_attribute("href")
    #product_link.append(link)


# find name
name = wd.find_element(by=By.XPATH, value='/html/body/main/div[3]/div[1]/section/div[2]/div/div[3]/div[1]/header/div/h1')
product_name.append(name.text)

# find ASIN number
#data_asin = wd.get_attribute("data-asin")
#product_asin.append(data_asin)

# find price
price = wd.find_element(by=By.XPATH, value='.//span[@id="pdp-cur-price"]').text
product_price.append(price)

# find ratings box
#ratings_box = item.find_elements(by=By.XPATH, value='.//div[@class="a-row a-size-small"]/span')

# find ratings and ratings_num
#if ratings_box != []:
   #ratings = ratings_box[0].get_attribute('aria-label')
   #ratings_num = ratings_box[1].get_attribute('aria-label')
#else:
   #ratings, ratings_num = 0, 0

#product_ratings.append(ratings)
#product_ratings_num.append(str(ratings_num))

    # find link
    #link = item.find_element(by=By.XPATH, value='.//a[@class="a-link-normal a-text-normal"]').get_attribute("href")
    #product_link.append(link)

wd.quit()

# to check data scraped
print(product_name)
#print(product_asin)
print(product_price)
#print(product_ratings)
#print(product_ratings_num)
#print(product_link)

class BookSale:
    int price
    String DeliveryDate
    int numReviews
    int avgReview

    int priceRank
    String deliveryDaterank
