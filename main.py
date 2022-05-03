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
search_bar.send_keys("978-1071614174")
time.sleep(5)
search_button = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input")
search_button.click()
time.sleep(15)

product_name = []
#product_asin = []
product_price = []
#product_ratings = []
#product_ratings_num = []
product_link = []

items_all = wait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
items_sponsored = wait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "AdHolder")]')))
items = [item for item in items_all if item not in items_sponsored]
for item in items:
    # find name
    name = item.find_element(by=By.XPATH, value='.//span[@class="a-size-medium a-color-base a-text-normal"]')
    product_name.append(name.text)

    # find ASIN number
    #data_asin = item.get_attribute("data-asin")
    #product_asin.append(data_asin)

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
    #if ratings_box != []:
        #ratings = ratings_box[0].get_attribute('aria-label')
        #ratings_num = ratings_box[1].get_attribute('aria-label')
    #else:
        #ratings, ratings_num = 0, 0

    #product_ratings.append(ratings)
    #product_ratings_num.append(str(ratings_num))

    # find link
    link = item.find_element(by=By.XPATH, value='.//a[contains(@class,"a-link-normal")]').get_attribute("href")
    product_link.append(link)

wd.get(product_link[0])

all_sellers_button = wd.find_element(By.XPATH, '//*[@id="a-autoid-2"]/span')
all_sellers_button.click()

time.sleep(5)

see_more_button = wd.find_element(By.XPATH, '//*[@id="aod-pinned-offer-show-more-link"]')
see_more_button.click()

#time.sleep(3)

pinned_offer = wd.find_element(By.XPATH, '//*[@id="aod-pinned-offer"]')
main_seller_object_info = pinned_offer.find_element(By.XPATH, '//*[@id="aod-pinned-offer-additional-content"]')
main_seller_name = main_seller_object_info.find_element(By.XPATH, './/*[@id="aod-offer-shipsFrom"]/div/div/div[2]/span').text
main_seller_ratings_text = main_seller_object_info.find_element(By.XPATH, './/*[@id="seller-rating-count-{iter}"]/span').text
main_seller_rating = main_seller_ratings_text.split("%")[0][-2:]
main_num_ratings = main_seller_ratings_text.split(" ")[0][1:]
main_seller_delivery_day = pinned_offer.find_element(By.XPATH, './/*[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]/span/span').text
#main_seller_delivery_date = main_seller_delivery_day.split(', ')[1]
main_seller_add_cart = pinned_offer.find_element(By.XPATH, './/*[@id="a-autoid-2-offer-0"]/span/input')
main_seller_add_cart.click()
main_whole_price = pinned_offer.find_elements(by=By.XPATH, value='.//span[@class="a-price-whole"]')
main_fraction_price = pinned_offer.find_elements(by=By.XPATH, value='.//span[@class="a-price-fraction"]')

if main_whole_price != [] and main_fraction_price != []:
    main_sellerPrice = '.'.join([main_whole_price[0].text, main_fraction_price[0].text])
else:
    main_sellerPrice = 0

print("Main Seller Name: " + main_seller_name)
print("Main Seller Delivery: " + main_seller_delivery_day)
print("Main Seller Rating: " +main_seller_rating)
print("Main Seller Num Ratings: " +main_num_ratings)
print("Main Seller Price: " + main_sellerPrice)


all_other_sellers = wait(wd, 50).until(EC.presence_of_all_elements_located((By.ID, 'aod-offer')))

for seller in all_other_sellers:

    sellerNameObject = seller.find_element(By.XPATH, './/*[@id="aod-offer-shipsFrom"]/div[@class="a-fixed-left-grid"]/div[@class="a-fixed-left-grid-inner"]/div[@class="a-fixed-left-grid-col a-col-right"]/span')
    sellerName = sellerNameObject.text
    print("Seller Name: " + sellerName)

    whole_price = seller.find_elements(by=By.XPATH, value='.//span[@class="a-price-whole"]')
    fraction_price = seller.find_elements(by=By.XPATH, value='.//span[@class="a-price-fraction"]')

    if whole_price != [] and fraction_price != []:
        sellerPrice = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        sellerPrice = 0
    print("Seller Price: " + sellerPrice)

    dayObject = seller.find_element(By.XPATH, './/*[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]/span/span[@class="a-text-bold"]')
    day = dayObject.text
    #date = day.split(' ')[1]
    print("Delivery date= "+day)

    try:
        sellerRatingObject = seller.find_element(By.XPATH, './/*[@id="aod-offer-seller-rating"]/span[@class="a-size-small a-color-base"]/span')
        sellerRatingText = sellerRatingObject.text
        sellerRatingText.replace('\n', '')
        #sellerRatingPercent = sellerRatingText.split("%")[0]
    except:
        sellerRatingText = None
        sellerRating = None
        numRatings = None
    sellerRating = sellerRatingText.split("%")[0][-2:]
    numRatings = sellerRatingText.split(" ")[0][1:]
    print("Seller Rating: " + sellerRating)
    print("Num Ratings: " + numRatings)

    sellerBookStatusObject = seller.find_element(By.XPATH, './/*[@id="aod-offer-heading"]')
    sellerBookStatus = sellerBookStatusObject.text
    print("Book condition: " + sellerBookStatus)

    addToCartButtonObject = seller.find_element(By.XPATH, './/*[@class="a-button a-button-primary aod-atc-generic-btn-desktop"]/span/input')
    print(addToCartButtonObject.get_attribute('aria-label'))

    addToCartButtonObject.click()

    print("\n")

time.sleep(5)

closeOtherSellers = wd.find_element(By.XPATH, '//*[@id="aod-close"]/span/span/i')
closeOtherSellers.click()

wd.get('https://www.amazon.com/gp/cart/view.html?ref_=nav_cart')

time.sleep(5)

proceedToCheckout = wd.find_element(By.XPATH, '//*[@id="sc-buy-box-ptc-button"]/span/input')
proceedToCheckout.click()

time.sleep(5)

signInBox = wd.find_element(By.XPATH, '//*[@id="ap_email"]')
signInBox.send_keys('')
signInContinueButton = wd.find_element(By.XPATH, '//*[@id="continue"]')
signInContinueButton.click()

time.sleep(5)

passwordBox = wd.find_element(By.XPATH, '//*[@id="ap_password"]')
passwordBox.send_keys('')
passwordSignInButton = wd.find_element(By.XPATH, '//*[@id="signInSubmit"]')
passwordSignInButton.click()

time.sleep(15)



#finalDealAddToCartButtonList = wd.find_elements(By.XPATH, '//*[@name="submit.addToCart"')

# to check data scraped
#print(product_name)
#print(product_asin)
#print(product_price)
#print(product_ratings)
#print(product_ratings_num)
#print(product_link)


wd.quit()