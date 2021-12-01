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

    def click_element(self, element):
        """ Click on an element based on a given element """
        self.action.move_to_element(element)
        self.action.click()
        self.action.perform()

    def click(self, xpath):
        """ Click on an element based on a given xpath """
        element = self.driver.find_element(By.XPATH, xpath)
        self.click_element(element)

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


class LichessBoard:
    xpath = None
    driver = None
    state = dict()


    def __init__(self, driver, xpath):
        super().__init__()
        self.driver = driver
        self.xpath = xpath

    def get_board_orientation(self):
        board_properties = self.driver.find_element(By.XPATH, self.xpath.get("orientation")).get_property("classList")
        for property in board_properties:
            if str(property) == "orientation-white" or str(property) == "orientation-black":
                return str(property)

        # throw error here as board does not seem to have a valid orientation
        return "fail"

    def get_cg_board(self):
        return self.driver.find_element(By.XPATH, self.xpath.get("state"))

    def get_board_pixel_size(self):
        """ Return the width x height of the board in pixels """
        board_size_element = self.driver.find_element(By.XPATH, self.xpath.get("pixel_size"))
        return [board_size_element.get_property("clientWidth"), board_size_element.get_property("clientHeight")]

    def get_square_pixel_size(self):
        board_pixel_size = self.get_board_pixel_size()
        return [board_pixel_size[0]/8, board_pixel_size[1]/8]

    def get_last_move(self):
        # Note: A better way would be to use linked-list property of web elements to get the corresponding nodes
        piece = ""
        last_move0 = ""
        last_move1 = ""
        for key, val in self.state.items():
            if (str(key) == "last-move0"):
                print(val)
                piece = str(self.state[val.get_property("cgKey")].get_property("cgPiece"))
                last_move0 = str(val.get_property("cgKey"))
            elif (str(key) == "last-move1"):
                last_move1 = str(val.get_property("cgKey"))

        return piece + last_move1 + last_move0




    def get_board_state(self):
        return self.state

    def update_board_state(self):
        """ The board state is a dictionary mapping position to web element (square/piece)"""
        self.state.clear()
        cg_board = self.get_cg_board()
        cg_board_properties = cg_board.get_property("childNodes")
        last_move = ""
        last_move_found = 0
        for cell in cg_board_properties:
            if (cell.get_property("className") == "last-move"):
                self.state["last-move" + str(last_move_found)] = cell
                last_move_found += 1
            else:
                self.state[str(cell.get_property("cgKey"))] = cell

        for key, value in self.state.items():
            print(key, " : ", value)





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
        "puzzles_moves_table"    : "//*[@id=\"main-wrap\"]/ main/div[2]/div[2]/div",
    }

    puzzles_board_xpath = {
        "pixel_size": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container",
        "orientation": "//*[@id=\"main-wrap\"]/main/div[1]/div",
        "state": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container/cg-board"
    }

    board = None

    def __init__(self):
        super().__init__()
        self.board = LichessBoard(self.driver, self.puzzles_board_xpath)

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

    def get_board(self):
        return self.board

    def get_puzzle_pgn(self):
        """ Returns the pgn of a puzzle in string format """
        moves_table = self.driver.find_element(By.XPATH, self.xpath.get("puzzles_moves_table"))

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


    def make_move(self, move):
        """
        :param move: string that is a move
        :return: None
        """
        pass


class LichessEngine(WebTester):
    url = "https://lichess.org/analysis"
    xpath = {
        "suggested_moves"   : "//*[@id=\"main-wrap\"]/main/div[3]/div[2]/div",
        "pgn_bar"           : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]",
        "pgn_button"        : "//*[@id=\"main-wrap\"]/main/div[5]/div/div[2]/div/button",
        "state"             : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/cg-board",
        "board_orientation" : "//*[@id=\"main-wrap\"]/main/div[1]/div[3]"
    }

    analysis_board_xpath = {
        "pixel_size": "//*[@id=\"main-wrap\"]/main/div[1]/div/cg-container",
        "orientation": "//*[@id=\"main-wrap\"]/main/div[1]/div[3]",
        "state": "//*[@id=\"main-wrap\"]/main/div[1]/div[3]/cg-container/cg-board"
    }

    board = None

    def __init__(self):
        super().__init__()
        self.board = LichessBoard(self.driver, self.analysis_board_xpath)

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
        best_move = suggested_moves.get_property("childNodes")[2]
        return best_move.get_property("innerText")

    @staticmethod
    def update_pgn(pgn, move):
        return pgn + move

    def get_board(self):
        return self.board

    def test(self):
        #print(list(self.get_board().get_board_state().values())[-1])
        cell = list(self.get_board().get_board_state().values())[-1]
        self.click_element(cell)

# https://lichess.org/analysis

if __name__ == '__main__':

    lichess_website_tester = LichessTester()
    lichess_website_tester.open_website()
    time.sleep(0.2)
    lichess_website_tester.click_puzzles()
    time.sleep(0.2)
    pgn = lichess_website_tester.get_puzzle_pgn()
    time.sleep(1)
    lichess_website_tester.get_board().update_board_state()
    print(lichess_website_tester.get_board().get_square_pixel_size())
    print(lichess_website_tester.get_board().get_board_orientation())
    print(lichess_website_tester.get_board().get_last_move())


    lichess_engine = LichessEngine()
    lichess_engine.open_website()
    lichess_engine.enable_engine()
    time.sleep(1)
    lichess_engine.import_pgn(pgn)
    time.sleep(1)
    lichess_engine.enter_pgn()
    time.sleep(2)
    best_move = lichess_engine.get_best_move()
    next_pgn = lichess_engine.update_pgn(pgn, best_move)
    time.sleep(1)
    lichess_engine.import_pgn(next_pgn)
    lichess_engine.enter_pgn()
    time.sleep(1)
    lichess_engine.get_board().update_board_state()
    print(lichess_engine.get_board().get_square_pixel_size())
    print(lichess_engine.get_board().get_board_orientation())
    print(lichess_engine.get_board().get_last_move())
    print(lichess_engine.get_board().get_board_state())
    lichess_engine.test()



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

#iterate till find 'black' or 'white'

#https://lichess.org/forum/lichess-feedback/play-by-typing-san-moves-like-e4-nf3-or-qxd6


# To translate pieces to position need to consider:
# board flip position   | # //*[@id="main-wrap"]/main/div[1]/div .get_property("innerText") == black/white
# board size            |
# piece position        |



#1) Every time a higher ranking pieces moves, a capital prefix is apparent
#2) Pawns have no capital prefix
#3) If multiple pieces can enter a square, the piece to enter the square is specified by the file and x


# Just use last move information


# After getting best move, make it. Then record the previous move to get c1n1c2n2
# After making the best move, wait for computer response. Then record c1n1c2n2