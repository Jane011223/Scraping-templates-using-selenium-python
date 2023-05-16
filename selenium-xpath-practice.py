import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time 
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
#import openpyxl

product_links = []
product_names = []
product_prices = []
product_descriptions = []
product_imglinks = []

options = Options()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

page_url = "https://www.bradburnhome.com/collections/casual"

driver.get(page_url)

names = driver.find_element(By.XPATH, '//*[@id="shopify-section-collection-template"]').find_elements(By.XPATH, './div')

ht = names[0].find_element(By.TAG_NAME, 'h1').get_attribute('innerHTML')

print(ht)

	