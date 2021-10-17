from selenium import webdriver
from selenium.webdriver.chrome.service import Service

LICHESS_URL = "https://lichess.org"
CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)

driver = webdriver.Chrome(service=SERVICE)
driver.get(LICHESS_URL)

if __name__ == '__main__':
    pass


