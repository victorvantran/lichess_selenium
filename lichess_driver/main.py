from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  # Gives access to input keys to interface with the website
from selenium.webdriver.common.by import By  # Allows us to identify the xpath of element
from selenium.webdriver.common.action_chains import \
    ActionChains  # Allows us to perform generic actions on modules such as hovering, clicking, etc.
from selenium.webdriver.support.ui import WebDriverWait # Allows us to stall the driver to wait for a particular element to load
from selenium.webdriver.support import expected_conditions as EC
import time  # Allows us to sleep for a certain number of seconds



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


    def press_key(self, key):
        """ Press a key """
        self.action.send_keys(key)
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
        "search_bar"    : "//header[@id='top']//div[@class='site-buttons']//div[@id='clinput']//a[@class='link']", \
        # specify the element by multiple identifiers, separated by '//'
        "moves_table"   : "// * [ @ id = \"main-wrap\"] / main / div[2] / div[2] / div"
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


    def get_puzzle_pgn(self):
        """ Returns the pgn of a puzzle in string format """
        moves_table = self.driver.find_element(By.XPATH, self.xpath.get("moves_table"))

        pgn = ""
        num_elements = moves_table.get_property("childElementCount")
        # [!] ASSUME THERE IS AT LEAST 1 MOVE MADE IN THE PUZZLE POSITION (NEED AN ASSERTION TO CHECK)

        for i in range(0, num_elements, 3):
            pgn += str(((i//3) + 1)) + ". "

            white_move = moves_table.get_property("childNodes")[i + 1]
            pgn += white_move.get_property("innerText") + " "

            if (white_move.get_attribute("class") != "hist"):
                break

            black_move = moves_table.get_property("childNodes")[i + 2]
            pgn += black_move.get_property("innerText") + " "

        return pgn




class LichessEngine(WebTester):
    url = "https://lichess.org/analysis"
    xpath = {
        "suggested_moves"   : "//*[@id=\"main-wrap\"]/main/div[3]/div[2]/div",
        "pgn_bar"           : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]",
        "pgn_button"        : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]/div/button"
    }

    def __init__(self):
        super().__init__()

    def open_website(self):
        """ Open a website given a URL """
        self.driver.get(self.url)

    def enable_engine(self):
        self.press_key(Keys.SPACE)


    def import_pgn(self, pgn):
        """ Import pgn to update analysis board """
        pgn_bar = self.driver.find_element(By.XPATH, self.xpath.get("pgn_bar"))
        self.action.move_to_element(pgn_bar)
        self.action.click()
        self.action.send_keys(pgn)
        self.action.perform()

    def enter_pgn(self):
        self.click(self.xpath.get("pgn_button"))


    def get_best_move(self):
        """ Return the best move in string format """
        suggested_moves = self.driver.find_element(By.XPATH, self.xpath.get("suggested_moves"))
        # [!] ASSUME THERE IS AT LEAST 1 MOVE ALWAYS SUGGESTED BY ENGINE (NEED AN ASSERTION TO CHECK)
        # NEED TO DELAY 2 SECONDS FOR ENGINE TO CALCULATE

        num_elements = suggested_moves.get_property("childElementCount")
        print(num_elements)
        best_move = suggested_moves.get_property("childNodes")[2]
        print(best_move.get_property("innerText"))






# https://lichess.org/analysis

if __name__ == '__main__':

    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(0.2)
    lichess_website_tester.click_puzzles()
    time.sleep(0.2)
    pgn = lichess_website_tester.get_puzzle_pgn()



    lichess_engine = LichessEngine()
    lichess_engine.open_website()
    lichess_engine.enable_engine()
    time.sleep(2)
    lichess_engine.import_pgn(pgn)
    time.sleep(3)
    lichess_engine.enter_pgn()
    time.sleep(2)
    lichess_engine.get_best_move()
    time.sleep(1000)


    """
    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(0.2)
    lichess_website_tester.click_puzzles()
    time.sleep(0.2)
    lichess_website_tester.get_puzzle_moves_table()
    time.sleep(1000)
    """



    """
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


# /html/body/div[1]/main/div[1]/div[3]/cg-container/cg-board