from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
import time
import csv

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# import undetected_chromedriver as uc
# # import time
# from webdriver_manager.chrome import ChromeDriverManager
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())

# driver.maximize_window()


driver = Chrome(options=options, executable_path=ChromeDriverManager().install())

driver.maximize_window()

component_titles = []
component_links = []
component_details = []
component_time = []
component_prices = []
write_result = []

driver.get("https://www.njuskalo.hr/auti/c-max")

time.sleep(10)

driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()

totalbox = driver.find_element(By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[7]/div[6]')

subcategories = totalbox.find_elements(By.CLASS_NAME, "entity-body")

for i in range(len(subcategories)):
    title = subcategories[i].find_element(By.TAG_NAME, "h3").text
    link = subcategories[i].find_element(By.CLASS_NAME, "entity-title").find_element(By.CLASS_NAME, "link").get_attribute("href")
    details = subcategories[i].find_element(By.CLASS_NAME, "entity-description-main").text
    times = subcategories[i].find_element(By.CLASS_NAME, "date--full").text
    price = subcategories[i].find_element(By.CLASS_NAME, "price--hrk").text
    print("-------------------------")
    print("Title--> ", title)
    print("Detail--> ", details)
    print("Time--> ", times)
    print("Price--> ", price)

    component_titles.append(title)
    component_links.append(link)
    component_details.append(details)
    component_time.append(times)
    component_prices.append(price)

    write_data = {}

    write_data["Title"] = title
    write_data["LInk"] = link
    write_data["Details"] = details
    write_data["Time"] = times
    write_data["Price"] = price

    write_result.append(write_data)

    dict = {'Title': component_titles, 'Link': component_links, 'Details': component_details, 'Time': component_time, 'Price': component_prices}
    df = pd.DataFrame(dict)

    df.to_csv('Result.csv', index = False)



    
driver.get("https://www.njuskalo.hr/auti/c-max?page=2")
time.sleep(10)

totalbox = driver.find_element(By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[7]/div[4]/ul')

subcategories = totalbox.find_elements(By.CLASS_NAME, "entity-body")

for i in range(len(subcategories)):
    title = subcategories[i].find_element(By.TAG_NAME, "h3").text
    link = subcategories[i].find_element(By.CLASS_NAME, "entity-title").find_element(By.CLASS_NAME, "link").get_attribute("href")
    details = subcategories[i].find_element(By.CLASS_NAME, "entity-description-main").text
    times = subcategories[i].find_element(By.CLASS_NAME, "date--full").text
    price = subcategories[i].find_element(By.CLASS_NAME, "price--hrk").text
    print("-------------------------")
    print("Title--> ", title)
    print("Detail--> ", details)
    print("Time--> ", times)
    print("Price--> ", price)

    # Open the CSV file in append mode
    with open('Result.csv', mode='a', newline='', encoding = 'utf-8') as file:
        writer = csv.writer(file)

        # Write the new row to the CSV file
        writer.writerow([title, link, details, times, price])

    print('Data appended to CSV file.')