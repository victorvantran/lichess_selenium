from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
import time  # Allows us to sleep for a certain number of seconds

# Constants
LICHESS_URL = "https://lichess.org"
CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)


class WebTester:
    driver = None
    action = None

    def __init__(self):
        self.driver = webdriver.Chrome(service=SERVICE)
        self.action = ActionChains(self.driver)

    def __del__(self):
        self.driver.close()

    def open_website(self, url):
        self.driver.get(LICHESS_URL)

    def click_puzzles(self):
        self.driver.find_element(By.XPATH, "//a[@href='/training']").click()

    def hover_puzzles(self):
        element = self.driver.find_element(By.XPATH, "//a[@href='/training']")
        self.action.move_to_element(element).perform()

    def click_puzzles_dashboard(self):
        self.hover_puzzles()
        sub_element = self.driver.find_element(By.XPATH, "//a[@href='/training/dashboard/30']")
        self.action.move_to_element(sub_element).click().perform()

    def click_puzzles_streak(self):
        self.hover_puzzles()
        sub_element = self.driver.find_element(By.XPATH, "//a[@href='/streak']")
        self.action.move_to_element(sub_element).click().perform()

    def click_puzzles_storm(self):
        self.hover_puzzles()
        sub_element = self.driver.find_element(By.XPATH, "//a[@href='/storm']")
        self.action.move_to_element(sub_element).click().perform()

    def click_puzzles_racer(self):
        self.hover_puzzles()
        sub_element = self.driver.find_element(By.XPATH, "//a[@href='/racer']")
        self.action.move_to_element(sub_element).click().perform()

        """
        BREAKING IT DOWN
        # https://www.tutorialspoint.com/how-can-i-perform-mouse-hover-action-in-selenium-python
        action = ActionChains(self.driver)
        # identify element
        element = self.driver.find_element(By.XPATH, "//a[@href='/training']")
        # hover over element
        action.move_to_element(element).perform()
        # identify sub menu element
        sub_element = self.driver.find_element(By.XPATH, "//a[@href='/racer']")
        # hover over element and click
        action.move_to_element(sub_element).click().perform()
        """


if __name__ == '__main__':
    web_tester = WebTester()
    web_tester.open_website(LICHESS_URL)
    time.sleep(3)
    web_tester.click_puzzles()
    time.sleep(3)
    web_tester.click_puzzles_dashboard()
    time.sleep(3)
    web_tester.click_puzzles_streak()
    time.sleep(3)
    web_tester.click_puzzles_storm()
    time.sleep(3)
    web_tester.click_puzzles_racer()
    time.sleep(3)