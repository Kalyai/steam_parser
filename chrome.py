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
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    )

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
