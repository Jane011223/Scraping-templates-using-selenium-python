from selenium import webdriver
from selenium.webdriver.chrome.options import Options

 # Set up the Chrome options
options = Options()
#options.add_argument(f'--proxy-server=socks5://64.225.28.9:52700')
 # Start the browser with the configured proxy settings
driver = webdriver.Chrome(options=options)
driver.get('https://affilisting.com/list')
# interact with the page as needed

filename = 'screenshot.png'
driver.get_screenshot_as_file(filename)

