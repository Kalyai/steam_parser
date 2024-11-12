from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def driver_init():
    chromedriver_path = '/Users/sergeikalyaev/Downloads/chromedriver-mac-arm64_2/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir="/Users/sergeikalyaev/Library/Application Support/Google/Chrome"')
    chrome_options.add_argument('--profile-directory="Profile 1"')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
