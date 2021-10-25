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
        """ Open a website given a URL """
        self.driver.get(LICHESS_URL)

    def hover(self, xpath):
        """ Hover over a module based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.perform()

    def hover_puzzles(self):
        """ Hover over the Puzzles tab on the top bar menu """
        self.hover("//a[@href='/training']")

    def click(self, xpath):
        """ Click on a module based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.click()
        self.action.perform()

    def click_puzzles(self):
        """ Click on the Puzzles tab on the top bar menu """
        self.click("//a[@href='/training']")

    def click_puzzles_dashboard(self):
        """ Click on the Puzzles Dashboard button under the Puzzles tab """
        self.hover_puzzles()
        self.click("//a[@href='/training/dashboard/30']")

    def click_puzzles_streak(self):
        """ Click on the Puzzles Streak button under the Puzzles tab """
        self.hover_puzzles()
        self.click("//a[@href='/streak']")

    def click_puzzles_storm(self):
        """ Click on the Puzzles Storm button under the Puzzles tab """
        self.hover_puzzles()
        self.click("//a[@href='/storm']")

    def click_puzzles_racer(self):
        """ Click on the Puzzles Racer button under the Puzzles tab """
        self.hover_puzzles()
        self.click("//a[@href='/racer']")

    def search(self, string_input):
        """ Search given an input """
        search_bar = self.driver.find_element(By.XPATH, "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']")   # specify the element by multiple identifiers, separated by '//'
        self.action.move_to_element(search_bar)
        self.action.click()
        self.action.send_keys(string_input)
        self.action.perform()
        time.sleep(1)   # delay so we can see the input on the search bar
        self.action.send_keys(Keys.RETURN)
        self.action.perform()
        # self.action.move_to_element(element).click().send_keys(input).send_keys(Keys.RETURN).perform() # one liner



if __name__ == '__main__':
    web_tester = WebTester()
    web_tester.open_website(LICHESS_URL)
    time.sleep(2)
    web_tester.click_puzzles()
    time.sleep(2)
    web_tester.click_puzzles_dashboard()
    time.sleep(2)
    web_tester.click_puzzles_streak()
    time.sleep(2)
    web_tester.click_puzzles_storm()
    time.sleep(2)
    web_tester.click_puzzles_racer()
    time.sleep(2)
    web_tester.search("Hello, world!")
    time.sleep(10)


"""
SUBMENU CLICK
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