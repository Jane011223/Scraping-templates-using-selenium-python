from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import pandas as pd
import time
from random import randrange
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import json
import re

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--disable-features=NetworkService')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--blink-settings=imagesEnabled=false')

# # set network conditions to disable css and images
# network_conditions = {
#     'offline': False,
#     'latency': 5,  # additional latency (ms)
#     'download_throughput': 500 * 1024,  # download speed (bytes/s)
#     'upload_throughput': 500 * 1024  # upload speed (bytes/s)
# }
# options.set_network_conditions(offline=False, **network_conditions)

driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
driver.maximize_window()

LOGIN_URL = "https://affilisting.com/login"
modal_xpath = '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[3]/dl'
close_xpath = '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[1]/button'
dropdown_xpath = '//*[@id="filter-section-0"]/div/div/div[1]/button'
ul_xpath = '//*[@id="options"]'

tags_file = open('tags.txt', 'w')
programs_file = open('products.txt', 'w')
platforms_file = open('platforms.txt', 'w')
geolocations_file = open('geolocations.txt', 'w', encoding='utf-8')


# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["mydatabase"]

def log_in():
    driver.get(LOGIN_URL)
    time.sleep(10)

    email = "waynapayer@gmail.com"
    password = "Malitr$$324olr"

    email_field = driver.find_element(By.ID, 'email')
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[4]/button')
    submit_btn.click()

    time.sleep(20)


def get_tags():
    #get the tags
    dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[1]/h3/button'
    
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    # # Wait for the element to become interactable
    # wait = WebDriverWait(driver, 10)
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))

    btn.click()
    time.sleep(5)

    btn = driver.find_element(By.XPATH, dropdown_xpath)
    btn.click()
    time.sleep(5)
    lists = driver.find_element(By.XPATH, ul_xpath).find_elements(By.TAG_NAME, 'li')
    for i in range(len(lists)):
        element = lists[i]
        text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
        tags_file.write(text + '\n')

    tags_file.close()

    btn.click()
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    btn.click()
    time.sleep(5)
    print("tags scraping success")

def get_platforms():
    #get the platforms
    dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[2]/h3/button'
    
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    btn.click()
    time.sleep(5)

    btn = driver.find_element(By.XPATH, '//*[@id="filter-section-0"]/div/div/div[1]/button')
    btn.click()
    time.sleep(5)
    lists = driver.find_element(By.XPATH, ul_xpath).find_elements(By.TAG_NAME, 'li')
    for i in range(len(lists)):
        element = lists[i]
        text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
        platforms_file.write(text + '\n')

    platforms_file.close()

    btn.click()
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    btn.click()
    time.sleep(5)

    print("platforms scraping success")

def get_geolocations():
    #get the geolocations
    dropdown1_xpath = '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[1]/div/div/div[3]/h3/button'
    
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    btn.click()
    time.sleep(5)

    btn = driver.find_element(By.XPATH, dropdown_xpath)
    btn.click()
    time.sleep(5)
    lists = driver.find_element(By.XPATH, ul_xpath).find_elements(By.TAG_NAME, 'li')
    for i in range(len(lists)):
        element = lists[i]
        text = element.find_element(By.TAG_NAME, 'span').get_attribute('innerText')
        geolocations_file.write(text + '\n')

    geolocations_file.close()

    btn.click()
    btn = driver.find_element(By.XPATH, dropdown1_xpath)
    btn.click()
    time.sleep(5)

    print("geolocations scraping success")


def get_elements(element):
    title = element.find_elements(By.TAG_NAME, 'td')[0].find_elements(By.TAG_NAME, 'div')[0].get_attribute('innerText')
    
    product_link = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/a')
    # product_link = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/a').get_attribute('href')
    # print(product_link)

    # open the URL in a new tab
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).click(product_link).key_up(Keys.CONTROL).perform()

    # switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)
    # get the URL of the new tab
    product_link = driver.current_url

    # do something with the new URL
    # print(product_link)

    # close the new tab
    driver.close()

    # switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])

    elements = driver.find_element(By.XPATH, modal_xpath).find_elements(By.TAG_NAME, "dd")
    affilication_type = elements[0].get_attribute('innerText')
    affilication_platform = elements[1].get_attribute('innerText')
    # if(affilication_platform.contains("</a>")):
    #     affilication_platform = elements[1].find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')
    product_type = elements[2].get_attribute('innerText')
    geolocation = elements[3].find_element(By.TAG_NAME, 'div').get_attribute('innerText')
    # if geolocation.contains("<div>"):
    #     geolocation = ""
    commission_0 = elements[4].get_attribute('innerText')
    commission_1 = elements[5].get_attribute('innerText')

    rounds = []
    round_elements = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div[2]/div[2]/div/div/div/div[2]/div/div[4]/div/ul').find_elements(By.TAG_NAME, 'span')
    for i in range(len(round_elements)):
        round_element = round_elements[i].get_attribute('innerText')
        rounds.append(round_element)
    
    data = {"title": title, "type": affilication_type, "platform": affilication_platform, "product_type": product_type, "product_link": product_link, "geolocation": geolocation, "commission_0": commission_0, "commission_1": commission_1, "tags": rounds}
    
    numbers = re.findall(r'\d+\.\d+|\d+', commission_0)
    if(len(numbers) > 0):
        number = float(numbers[0])
        data['num_commission_0'] = number

    numbers = re.findall(r'\d+\.\d+|\d+', commission_1)
    if(len(numbers) > 0):
        number = float(numbers[0])
        data['num_commission_1'] = number

    json.dump(data, programs_file)
    programs_file.write('\n')

def get_programdata():

    tr_elements = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for i in range(len(tr_elements)):
        tr_element = tr_elements[i]
        tr_element.click()

        #get elements from modal
        get_elements(tr_element)

        driver.find_element(By.XPATH, close_xpath).click()
    # try:
    #     #get the programs
    #     tr_elements = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    #     for i in range(len(tr_elements)):
    #         tr_element = tr_elements[i]
    #         tr_element.click()

    #         #get elements from modal
    #         get_elements(tr_element)

    #         driver.find_element(By.XPATH, close_xpath).click()
            
    # except:
    #     print("error")
    
def get_random_rgbcolor():
    r = random.randint(100,255)
    g = random.randint(100,255)
    b = random.randint(100,255)
    rgb = "rgb" + str((r,g,b))
    return rgb;

def setStatus(status):
    # Find the first document in the collection and update it
    collection = db["schedules"]
    query = {}
    new_values = { "$set": { "running": status } }
    updated_doc = collection.find_one_and_update(query, new_values)
    # Print the updated document
    print(updated_doc)

def save_into_database():
    # Check if the collection exists
    if 'products' in db.list_collection_names():
        program_collection = db['products']
        program_collection.drop()

    if 'tags' in db.list_collection_names():
        tag_collection = db['tags']
        tag_collection.drop()

    if 'platforms' in db.list_collection_names():
        platform_collection = db['platforms']
        platform_collection.drop()

    if 'geolocations' in db.list_collection_names():
        geolocation_collection = db['geolocations']
        geolocation_collection.drop()

    program_collection = db.create_collection('products')
    tag_collection = db.create_collection('tags')
    platform_collection = db.create_collection('platforms')
    geolocation_collection = db.create_collection('geolocations')

    # Open a file in read mode
    tag_file = open('tags.txt', 'r')

    # Read the lines from the tags file
    for category in tag_file:
        color = get_random_rgbcolor()
        data = {"category": category, "color": color}
        tag_collection.insert_one(data)

    # Close the file
    tag_file.close()

    # Open a file in read mode
    platform_file = open('platforms.txt', 'r')

    # Read the lines from the platform file
    for platform in platform_file:
        data = {"platform" : platform}
        platform_collection.insert_one(data)

    # Close the file
    platform_file.close()

    # Open a file in read mode
    geolocation_file = open('geolocations.txt', 'r',  encoding='utf-8')

    # Read the lines from the geolocation file
    for geolocation in geolocation_file:
        data = {"geolocation" : geolocation}
        geolocation_collection.insert_one(data)

    # Close the file
    geolocation_file.close()

    # Open a file in read mode
    pro_file = open('products.txt', 'r')

    # Read the lines from the products file
    for program in pro_file:
        program_str = json.loads(program)
        program_collection.insert_one(program_str)

    # Close the file
    pro_file.close()

def scrape_site():
    time.sleep(10)
    get_tags()
    get_platforms()
    get_geolocations()
    get_programdata()

    page_num = 0
    next_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button')
    while next_btn:
        page_num += 1
        print(page_num)
        next_btn.click()
        time.sleep(10)
        get_programdata()

        try:
            next_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/main/div/div/div[2]/div/main/section/div/div[2]/div[2]/div[1]/div[3]/div/div/div/nav/div[2]/button[2]')
        except:
            next_btn = None

    programs_file.close()

    print("Scraping Success")
    save_into_database()
    print("Saved Success")



def main():
    setStatus(True)
    log_in()
    scrape_site()
    setStatus(False)

if __name__ == '__main__':
    main()

