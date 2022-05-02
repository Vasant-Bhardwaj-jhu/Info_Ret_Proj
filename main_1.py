from selenium import webdriver as wd
import requests
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time

options = wd.ChromeOptions()
options.add_argument('--headless')

# Getting data from Barnes and Noble
wd = wd.Chrome()

wd.implicitly_wait(10)
wd.get("https://www.barnesandnoble.com/")
search_bar = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/nav/div/div[3]/form/div/div[2]/div/input[1]")
time.sleep(5)
search_bar.send_keys("978-1071614174")
time.sleep(5)
search_button = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/nav/div/div[3]/form/div/span/button")
search_button.click()
time.sleep(7)

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
product_name = name.text

# find price
price = wd.find_element(by=By.XPATH, value='.//span[@id="pdp-cur-price"]').text
product_price = float(price[1:])

deliveryDay = wd.find_element(By.XPATH, './/*[@id="commerce-zone"]/div[2]/div[3]/div/span[2]/span').text
deliveryDate = deliveryDay.split(', ')[1]

time.sleep(5)

#addToCartButton = wd.find_element(By.XPATH, '//*[@id="skuSelection"]/div[1]/form/input[5]')
addToCartButton = wait(wd, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="skuSelection"]/div[1]/form/input[5]')))
addToCartButton.send_keys("\n")
#addToCartButton.click()

time.sleep(10)

cartButton = wd.find_element(By.XPATH, '//*[@id="viewShoppingBag"]')
cartButton.click()

time.sleep(10)

#checkoutButton = wd.find_element(By.XPATH, '//*[@id="checkoutForm"]/a')
#checkoutButton.click()

time.sleep(5)

#shoppingCartButton = wd.find_element(By.XPATH, '//*[@id="rhf_header_element"]/nav/div/div[3]/ul/li[2]')
#shoppingCartButton.click();

#time.sleep(5)

#continueToCheckout = wd.find_element(By.XPATH, '//*[@id="checkoutForm"]/a')
#continueToCheckout.click()


wd.get('https://www.barnesandnoble.com/checkout/guest-checkout.jsp')

time.sleep(5)

firstNameBox = wd.find_element(By.XPATH, '//*[@id="firstName"]')
lastNameBox = wd.find_element(By.XPATH, '//*[@id="lastName"]')
streetAddressBox = wd.find_element(By.XPATH, '//*[@id="streetAddress"]')

firstNameBox.send_keys("Saketh")
lastNameBox.send_keys("Manda")
streetAddressBox.send_keys("3700 North Charles St")

time.sleep(15)


wd.quit()

# to check data scraped
print(product_name)
print(product_price)
print(deliveryDate)