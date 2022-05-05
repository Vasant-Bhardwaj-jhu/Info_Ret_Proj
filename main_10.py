from selenium import webdriver as wd
import requests
from bs4 import BeautifulSoup
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import time


class Seller:
    website: str
    sellerName: str
    sellerPrice: float
    sellerRating: int
    numSellerRatings: int
    sellerAddToCart: WebElement
    bookCondition: str
