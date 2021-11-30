from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # Gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
from selenium.webdriver.support.ui import WebDriverWait # Allows us to stall the driver to wait for a particular element to load
from selenium.webdriver.support import expected_conditions as EC
import time  # Allows us to sleep for a certain number of seconds



# Constants
LICHESS_URL = "https://lichess.org"
CHROMEDRIVER_PATH = "D:\\Software Expert\\chromedriver.exe"
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
        """ Hover over an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.perform()

    def hover_puzzles(self):
        """ Hover over the Puzzles tab on the top bar menu """
        self.hover(XPATH_PUZZLES)

    def click(self, xpath):
        """ Click on an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.action.move_to_element(element)
        self.action.click()
        self.action.perform()

    def click_puzzles(self):
        """ Click on the Puzzles tab on the top bar menu """
        self.click(XPATH_PUZZLES)

    def click_puzzles_dashboard(self):
        """ Click on the Puzzles Dashboard button under the Puzzles tab """
        self.hover_puzzles()
        self.click(XPATH_PUZZLES_DASHBOARD)

    def click_puzzles_streak(self):
        """ Click on the Puzzles Streak button under the Puzzles tab """
        self.hover_puzzles()
        self.click(XPATH_PUZZLES_STREAK)

    def click_puzzles_storm(self):
        """ Click on the Puzzles Storm button under the Puzzles tab """
        self.hover_puzzles()
        self.click(XPATH_PUZZLES_STORM)

    def click_puzzles_racer(self):
        """ Click on the Puzzles Racer button under the Puzzles tab """
        self.hover_puzzles()
        self.click(XPATH_PUZZLES_RACER)

    def chrome_window_maximize(self):
        #options = webdriver.ChromeOptions()
        #options.add_argument("--start-maximized")
        #driver = webdriver.ChromeDriver(options)
        self.driver.maximize_window()

    def search(self, string_input):
        """ Search given an input """
        search_bar = self.driver.find_element(By.XPATH, XPATH_SEARCH_BAR)
        self.action.move_to_element(search_bar)
        self.action.click()
        self.action.send_keys(string_input)
        self.action.perform()
        time.sleep(1)   # delay so we can see the input on the search bar
        self.action.send_keys(Keys.RETURN)
        self.action.perform()
        # self.action.move_to_element(element).click().send_keys(input).send_keys(Keys.RETURN).perform() # one liner

    def wait_for(self, xpath):
        """ Waits for an element, given by its xpath, to appear on the page before proceeding """
        try:
            element = WebDriverWait(self.driver, MAX_WAIT_FOR_SECONDS).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except Exception as error:
            print('Error: {}'.format(error))
            self.driver.quit()


if __name__ == '__main__':
    web_tester = WebTester()
    web_tester.chrome_window_maximize()
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