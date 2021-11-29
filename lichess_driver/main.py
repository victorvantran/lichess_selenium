from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # Gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
from selenium.webdriver.support.ui import WebDriverWait # Allows us to stall the driver to wait for a particular element to load
from selenium.webdriver.support import expected_conditions as EC
import time  # Allows us to sleep for a certain number of seconds


"""
# Constants
LICHESS_URL = "https://lichess.org"
#CHROMEDRIVER_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)
MAX_WAIT_FOR_SECONDS = 10

# XPATHS
XPATH_PUZZLES = "//a[@href='/training']"
XPATH_PUZZLES_DASHBOARD = "//a[@href='/training/dashboard/30']"
XPATH_PUZZLES_STREAK = "//a[@href='/streak']"
XPATH_PUZZLES_STORM = "//a[@href='/storm']"
XPATH_PUZZLES_RACER = "//a[@href='/racer']"
XPATH_SEARCH_BAR = "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']" \
    # specify the element by multiple identifiers, separated by '//'
"""


CHROMEDRIVER_PATH = "E:\\chromedriver\\chromedriver.exe"
SERVICE = Service(CHROMEDRIVER_PATH)
MAX_WAIT_FOR_SECONDS = 10

class WebTester:
    driver = None
    action = None

    def __init__(self):
        self.driver = webdriver.Chrome(service=SERVICE)
        self.chrome_window_maximize()
        self.action = ActionChains(self.driver)

    def __del__(self):
        self.driver.close()


    def chrome_window_maximize(self):
        """ Maximize the chrome window """
        self.driver.maximize_window()


    def hover(self, xpath):
        """ Hover over an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.perform()


    def click(self, xpath):
        """ Click on an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.click()
        self.action.perform()


    def wait_for(self, xpath):
        """ Waits for an element, given by its xpath, to appear on the page before proceeding """
        try:
            element = WebDriverWait(self.driver, MAX_WAIT_FOR_SECONDS).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as error:
            print('Error: {}'.format(error))
            self.driver.quit()



class LichessTester(WebTester):
    url = "https://lichess.org"
    xpath = {
        "puzzles"       : "//a[@href='/training']",
        "dashboard"     : "//a[@href='/training/dashboard/30']",
        "streak"        : "//a[@href='/streak']",
        "storm"         : "//a[@href='/storm']",
        "racer"         : "//a[@href='/racer']",
        "search_bar"    : "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']" \
        # specify the element by multiple identifiers, separated by '//'
    }

    def __init__(self):
        super().__init__()

    def open_website(self):
        """ Open a website given a URL """
        self.driver.get(self.url)

    def hover_puzzles(self):
        """ Hover over the Puzzles tab on the top bar menu """
        self.hover(self.xpath.get("puzzles"))

    def click_puzzles(self):
        """ Click on the Puzzles tab on the top bar menu """
        self.click(self.xpath.get("puzzles"))

    def click_puzzles_dashboard(self):
        """ Click on the Puzzles Dashboard button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("streak"))

    def click_puzzles_streak(self):
        """ Click on the Puzzles Streak button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("streak"))

    def click_puzzles_storm(self):
        """ Click on the Puzzles Storm button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("storm"))

    def click_puzzles_racer(self):
        """ Click on the Puzzles Racer button under the Puzzles tab """
        self.hover_puzzles()
        self.click(self.xpath.get("racer"))

    def search(self, string_input):
        """ Search given an input """
        search_bar = self.driver.find_element(By.XPATH, self.xpath.get("search_bar"))
        self.action.move_to_element(search_bar)
        self.action.click()
        self.action.send_keys(string_input)
        self.action.perform()
        time.sleep(1)   # delay so we can see the input on the search bar
        self.action.send_keys(Keys.RETURN)
        self.action.perform()
        # self.action.move_to_element(element).click().send_keys(input).send_keys(Keys.RETURN).perform() # one liner






if __name__ == '__main__':
    lichess_tester = LichessTester()
    lichess_tester.open_website()
    time.sleep(2)
    lichess_tester.click_puzzles()
    time.sleep(2)
    lichess_tester.click_puzzles_dashboard()
    time.sleep(2)
    lichess_tester.click_puzzles_streak()
    time.sleep(2)
    lichess_tester.click_puzzles_storm()
    time.sleep(2)
    lichess_tester.click_puzzles_racer()
    time.sleep(2)
    lichess_tester.search("Hello, world!")
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